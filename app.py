from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import os
from fastapi.responses import JSONResponse
from typing import List
import re

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
tokenizer = None

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
        sentiment_pipeline = pipeline("sentiment-analysis", model=sentiment_model_path, framework='pt')

def load_classifier_model():
    global classifier_model, tokenizer
    if classifier_model is None:
        classifier_model_path = "models/fine_tuned_distilbart_mnli"
        classifier_model = AutoModelForSequenceClassification.from_pretrained(classifier_model_path)
        tokenizer = AutoTokenizer.from_pretrained(classifier_model_path)

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
    menu_item: str

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
async def greet(chat_request: UserMoodRequest):
    global sentiment_pipeline

    load_sentiment_pipeline()

    user_input = chat_request.user_mood_request.strip().lower()
    sentiment = determine_sentiment(user_input)
    response = generate_response(sentiment)

    return {"response": response}

@app.post("/ask_menu/", response_model=MenuResponse)
async def ask_menu(request: MenuRequest):
    global qa_pipeline

    load_qa_pipeline()

    user_menu_request = request.user_menu_request.strip().lower()
    menu_item = ask_question(user_menu_request, "What menu item do you want to order?")
    
    return MenuResponse(menu=menu_item)

@app.post("/ask_quantity/", response_model=QuantityResponse)
async def ask_quantity(request: QuantityRequest):
    global qa_pipeline

    load_qa_pipeline()

    context = request.user_quantity_request.strip().lower()
    question = f"How many {request.menu} does the customer want to order?"
    quantity = ask_question(context, question)

    return QuantityResponse(quantity=quantity)

# Add the endpoint to ask about the available menu
@app.get("/available_menu/")
async def available_menu():
    # Join the available menu items into a readable sentence
    menu_text = ", ".join(available_menu_items[:-1]) + ", and " + available_menu_items[-1]
    response_text = f"We currently have {menu_text}."

    return {"response": response_text}

@app.post("/ask_price/", response_model=PriceResponse)
async def ask_price(request: PriceRequest):
    global qa_pipeline

    load_qa_pipeline()

    # Extract the menu item using the question-answer pipeline
    menu_item = ask_question(request.menu_item, "What menu item is being asked about?")
    menu_item = menu_item.strip().lower()

    # Compile a case-insensitive regex pattern for each menu item
    matches = [item for item in item_prices.keys() if re.search(menu_item, item, re.IGNORECASE)]

    if matches:
        # Take the first match found (most similar)
        best_match = matches[0]
        price = item_prices[best_match]
        response = f"The price of {best_match} is {price} dollars."
    else:
        response = f"Sorry, we don't have {menu_item} on the menu."

    return PriceResponse(price=response)

@app.post("/end_chat/")
async def order_summary(chat_request: EndChatRequest):
    global classifier_model

    load_classifier_model()

    user_input = chat_request.is_end_chat.strip().lower()
    if check_conversation_end(user_input):
        response = "Thank you for ordering! Have a great day!"
    else:
        response = "What else would you like to order?"

    return {"response": response}

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

    # Define the label names in the same order as they were used in training
    label_names = ["asking_availability_menu", "asking_price", "order_menu", "quantity_order", "giving_address", "cancel_order"]
    predicted_label = label_names[predicted_class_id]

    if predicted_label == "asking_availability_menu":
        response = "It seems like you're asking about the available menu items."
    elif predicted_label == "order_menu":
        response = "It looks like you're trying to place an order."
    elif predicted_label == "quantity_order":
        response = "It seems like you're specifying the quantity for your order."
    elif predicted_label == "asking_price":
        response = "It seems like you're asking for menu price."
    elif predicted_label == "cancel_order":
        response = "It seems like you want to cancel your order."
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
    classification_result = classifier_model(
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
