from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
import os
from fastapi.responses import JSONResponse
from typing import List
import re
from typing import Optional
import sys
import logging

# Get the path to the child directory
repository_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend/repository')
# Add the child directory to sys.path
sys.path.append(repository_path)

import backend.repository.order_repository as order_repository
import backend.repository.menu_repository as menu_repository
import backend.repository.db_util as db_util

# FastAPI initialization
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for all origins (you can restrict this to specific origins if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model variables
qa_pipeline = None
sentiment_pipeline = None
classifier_model = None
end_chat_classifier_model = None
tokenizer = None

# Initialize database
db_util.init_db()

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

# Load the QA model and tokenizer
def load_qa_pipeline():
    global qa_pipeline
    if qa_pipeline is None:
        qa_model_path = "models/qa"
        qa_pipeline = pipeline("question-answering", model=qa_model_path, tokenizer=qa_model_path, framework='pt')

def load_sentiment_pipeline():
    global sentiment_pipeline
    if sentiment_pipeline is None:
        sentiment_model_path = "models/sentiment"
        sentiment_pipeline = sentiment_pipeline("sentiment-analysis", model=sentiment_model_path, framework='pt')

def load_classifier_model():
    global classifier_model, tokenizer
    if classifier_model is None:
        classifier_model_path = "models/fine_tuned_distilbart_mnli"
        classifier_model = AutoModelForSequenceClassification.from_pretrained(classifier_model_path)
        tokenizer = AutoTokenizer.from_pretrained(classifier_model_path)

def load_end_chat_classifier_model():
    global end_chat_classifier_model
    end_chat_classifier_model = pipeline("zero-shot-classification", model="models/classifier")

# Define data models for chatbot
class UserMoodRequest(BaseModel):
    user_mood_request: str

class MenuRequest(BaseModel):
    user_menu_request: str

class MenuResponse(BaseModel):
    menu: str

class QuantityRequest(BaseModel):
    menu: str
    user_quantity_request: str

class QuantityResponse(BaseModel):
    quantity: str

class EndChatRequest(BaseModel):
    is_end_chat: str

class AvailableMenuResponse(BaseModel):
    items: List[str]

class ClassificationRequest(BaseModel):
    user_input: str

# Define the request and response models
class PriceRequest(BaseModel):
    user_input: str

class PriceResponse(BaseModel):
    price: str

class AddressRequest(BaseModel):
    address_input: str

class AddressResponse(BaseModel):
    address: str


# Predefined list of available menu items
available_menu_items = [
    "Spaghetti Bolognese",
    "Creamy Alfredo",
    "Caesar Salad",
    "Margherita Pizza",
    "Grilled Chicken Sandwich",
    "Lemonade",
    "Garlic Bread"
]

# Dictionary to store prices of menu items
item_prices = {
    "Spaghetti Bolognese": 12,
    "Creamy Alfredo": 15,
    "Caesar Salad": 10,
    "Margherita Pizza": 14,
    "Grilled Chicken Sandwich": 8,
    "Lemonade": 3,
    "Garlic Bread": 4
}

# Define the FastAPI routes
@app.get("/")
async def root():
    return {"message": "Welcome to the Conversational Chatbot API!"}

@app.post("/greet/")
async def greet(chat_request: UserMoodRequest) -> str:
    global sentiment_pipeline

    load_sentiment_pipeline()

    user_input = chat_request.user_mood_request.strip().lower()
    sentiment = determine_sentiment(user_input)
    response = generate_response(sentiment)

    return response

@app.post("/ask_menu/", response_model=MenuResponse)
async def ask_menu(request: MenuRequest) -> str:
    logger.info("Start adding an order")
    global qa_pipeline

    load_qa_pipeline()

    user_menu_request = request.user_menu_request.strip().lower()
    menu_item = ask_question(user_menu_request, "What menu item do you want to order?")

    menu = get_the_best_match_from_menu(menu_item)
    if not menu:
        return f"Sorry, we don't have {menu_item} on the menu"
    
    # Check if the user has already ordered the same menu. If so, ask the user for a quantity
    if order_repository.get_order_by_menu_id(menu.id):
        return f"Seems like you already ordered that menu. Anything else I can help you with?"

    # Add order into database (without quantity yet)
    order_repository.insert_order(menu.id)
    
    return f"Thank you, how many {menu_item} do you want?"

@app.post("/ask_quantity/", response_model=QuantityResponse)
async def ask_quantity(request: QuantityRequest) -> str:
    logger.info("Start adding a quantity")
    global qa_pipeline

    load_qa_pipeline()

    # If menu name is not mentioned, the user might refer to the last ordered menu.
    # In this case, we update the quantity of the last order
    last_order = order_repository.get_last_order()

    # If the user hasn't ordered anything. Return a clarifying response
    if not last_order:
        return "It seems like you haven't ordered anything. Could you please clarify?"
    
    # Update the order quantity
    context = request.user_quantity_request.strip().lower()
    question = f"How many {request.menu} does the customer want to order?"
    quantity = ask_question(context, question)
    order_repository.update_order_quantity(last_order.id, quantity)

    return f"Alright, is there anything else do you want?"

# Add the endpoint to ask about the available menu
@app.get("/available_menu/")
async def available_menu() -> str:
    logger.info("Start querying menu")
    # Get all available menus from database
    available_menus = [menu.menu_name for menu in menu_repository.get_all_menu()]

    # Join the available menu items into a readable sentence
    menu_text = ", ".join(available_menus[:-1]) + ", and " + available_menus[-1]
    response_text = f"We currently have {menu_text}."

    return response_text

@app.post("/ask_price/", response_model=PriceResponse)
async def ask_price(request: PriceRequest) -> str:
    logger.info("Start querying for price")
    menu_item = get_menu_from_prompt(request.user_input)

    # Get the best matching menu
    menu = get_the_best_match_from_menu(menu_item)
    if menu == None:
        return f"Sorry, we don't have {menu_item} on the menu."
    
    return f"The price of {menu.menu_name} is {menu.price} dollars."

async def cancel_order(user_input: str) -> str:
    logger.info("Start cancelling an order")
    menu_item = get_menu_from_prompt(prompt=user_input)

    if not menu_item:
        last_order = order_repository.get_last_order()

        # If the user hasn't ordered anything. Return a clarifying response
        if len(last_order) == 0:
            return "It seems like you haven't ordered anything. Could you please clarify?"
        
        # delete the last order
        order_repository.delete_order_by_id(last_order.id)
    else:
        # Check if the menu exists
        menu = get_the_best_match_from_menu(menu_item)
        if menu == None:
            return f"Sorry, we don't have {menu_item} on the menu."
        
        # Check if the user has ordered the menu
        order = order_repository.get_order_by_menu_id(menu_id=menu.id)
        if order == None:
            return "Seems like you didn't order that menu. Could you please clarify?"
        
        # Delete the order
        order_repository.delete_order_by_id(order_id=order.id)

    return "Alright, I have cancelled that order. Anything else?"
    

@app.post("/end_chat/")
async def order_summary(chat_request: EndChatRequest):
    global end_chat_classifier_model

    load_end_chat_classifier_model()

    user_input = chat_request.is_end_chat.strip().lower()
    response = ""
    if check_conversation_end(user_input):
        response = "Thank you for ordering! Have a great day!"
    else:
        response = "What else would you like to order?"

    return response

@app.post("/classify_intent/")
async def classify_intent(chat_request: ClassificationRequest):
    global classifier_model, tokenizer

    load_classifier_model()

    user_input = chat_request.user_input.strip().lower()
    
    # Tokenize the input
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True)

    # Ensure model is in evaluation mode
    classifier_model.eval()

    # Perform prediction
    with torch.no_grad():
        outputs = classifier_model(**inputs)
        logits = outputs.logits

    # Get the predicted label
    predicted_class_id = torch.argmax(logits, dim=-1).item()

    # # Check if the user has already successfully ordered any menu
    print(f"user input: {user_input}")
    last_order = order_repository.get_last_order()
    if last_order:
        incomplete_orders = order_repository.get_incomplete_orders()
        if not incomplete_orders and check_conversation_end(user_input):
            return {"response": await order_summary(EndChatRequest(is_end_chat=user_input))}

    # Define the label names in the same order as they were used in training
    label_names = ["asking_availability_menu", "asking_price", "order_menu", "quantity_order", "giving_address", "cancel_order"]
    predicted_label = label_names[predicted_class_id]

    if predicted_label == "asking_availability_menu":
        response = await available_menu()
    elif predicted_label == "order_menu":
        response = await ask_menu(request=MenuRequest(user_menu_request=user_input))
    elif predicted_label == "quantity_order":
        response = await ask_quantity(QuantityRequest(menu="", user_quantity_request=user_input))
    elif predicted_label == "asking_price":
        response = await ask_price(PriceRequest(user_input=user_input))
    elif predicted_label == "cancel_order":
        response = await cancel_order(user_input=user_input)
    elif predicted_label == "giving_address":
        response = "It seems like you are giving your address."
    else:
        response = "I'm not sure what you're asking. Could you please clarify?"

    return {"response": response}


@app.post("/giving_address/", response_model=AddressResponse)
async def giving_address(request: AddressRequest):
    global qa_pipeline

    load_qa_pipeline()

    # Extract the address using the question-answer pipeline
    address = ask_question(request.address_input, "What is the address provided by the user?")
    address = address.strip()

    return AddressResponse(address=address)

# Helper functions for the chatbot
def ask_question(context, question):
    result = qa_pipeline({
        "context": context,
        "question": question
    })
    return result['answer']

def determine_sentiment(user_input):
    sentiment_result = sentiment_pipeline(user_input)
    sentiment = sentiment_result[0]['label'].lower()
    return sentiment

def generate_response(sentiment):
    if sentiment == "positive":
        return "Wow, nice to hear that! What do you want to order today?"
    elif sentiment == "negative":
        return "I'm sorry to hear that. Maybe a nice meal can help! What do you want to order?"
    else:
        return "Thanks for sharing. What do you want to order today?"

def check_conversation_end(user_input):
    print("Start checking for conversation end")
    global end_chat_classifier_model

    if end_chat_classifier_model is None:
        load_end_chat_classifier_model()

    classification_result = end_chat_classifier_model(
        user_input,
        candidate_labels=["end conversation", "continue conversation"],
        hypothesis_template="This statement is about {}."
    )
    label = classification_result['labels'][0]
    return label == "end conversation"

def classify_user_input(user_input):
    classification_result = classifier_model(
        user_input,
        candidate_labels=["asking_availability_menu", "asking_price", "order_menu", "quantity_order", "giving_address", "cancel_order"],
        hypothesis_template="The user is {}."
    )
    label = classification_result['labels'][0]
    return label

# To be used when getting the quantity from user
def get_menu_from_prompt(prompt: str) -> str:
    global qa_pipeline

    load_qa_pipeline()

    # Extract the menu item using the question-answer pipeline
    # menu_item = ask_question(prompt, "What menu item is being asked about?")
    menu_item = ask_question(prompt, "What food menu is being asked about?")
    menu_item = menu_item.strip().lower()

    return menu_item

def get_the_best_match_from_menu(menu_item: str) -> Optional[menu_repository.MenuEntity]:

    # Get all menu from DB
    menus = menu_repository.get_all_menu()

    matches = [item for item in menus if re.search(menu_item, item.menu_name, re.IGNORECASE)]

    if matches:
        # Take the first match found (most similar)
        best_match = matches[0]
        return best_match
    else:
        return None

# if __name__ == "__main__":
#     load_qa_pipeline

#     qa_model_path = "models/qa"
#     qa_pipeline = pipeline("question-answering", model=qa_model_path, tokenizer=qa_model_path, framework='pt')

#     result = ask_question("I would like to order 3 boxes", "What food menu is being asked about?")
#     result = qa_pipeline({
#         "context": "I would like to order 3 boxes",
#         "question": "What food menu is being asked about? If the prompt does not mention any food menu, simply answer 'NO'"
#     })
#     print(result["answer"])