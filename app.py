from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import vosk
import wave
import json
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

# Load the Vosk model once to avoid reloading it for each request
model_path = 'models/vosk-model-small-en-us-0.15'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model path '{model_path}' not found.")
vosk_model = vosk.Model(model_path)

# Initialize model variables
qa_pipeline = None
sentiment_pipeline = None
classifier = None

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

def load_classifier():
    global classifier
    if classifier is None:
        classifier_model_path = "models/classifier"
        classifier = pipeline("zero-shot-classification", model=classifier_model_path, framework='pt')

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
    global classifier

    load_classifier()

    user_input = chat_request.is_end_chat.strip().lower()
    if check_conversation_end(user_input):
        response = "Thank you for ordering! Have a great day!"
    else:
        response = "What else would you like to order?"

    return {"response": response}

@app.post("/classify_intent/")
async def classify_intent(chat_request: ClassificationRequest):
    global classifier

    load_classifier()

    user_input = chat_request.user_input.strip().lower()
    
    # Print the input for debugging
    print(f"Received input for intent classification: '{user_input}'")

    label = classify_user_input(user_input)

    if label == "asking_availability_menu":
        response = "It seems like you're asking about the available menu items."
    elif label == "order_menu":
        response = "It looks like you're trying to place an order."
    elif label == "quantity_order":
        response = "It seems like you're specifying the quantity for your order."
    elif label == "asking_price":
        response = "It seems like you're asking for menu price."
    elif label == "cancel_order":
        response = "It seems like you want to cancel your order."
    elif label == "giving_address":
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

@app.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    # Check if the uploaded file is a WAV file
    if not file.filename.endswith(".wav"):
        raise HTTPException(status_code=400, detail="Only WAV files are supported.")

    # Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Open the WAV file and process it
    try:
        with wave.open(temp_file_path, "rb") as wf:
            # Check if the WAV file has the expected format
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != 'NONE':
                raise HTTPException(status_code=400, detail="Audio file must be WAV format mono PCM.")

            # Initialize the recognizer with the sample rate from the WAV file
            recognizer = vosk.KaldiRecognizer(vosk_model, wf.getframerate())

            # Read the audio data and process it
            while True:
                data = wf.readframes(4000)  # Read data in chunks
                if len(data) == 0:
                    break
                recognizer.AcceptWaveform(data)

            # Get the final result
            final_result = recognizer.FinalResult()
            text = json.loads(final_result).get("text", "")
            return JSONResponse(content={"recognized_text": text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

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
    classification_result = classifier(
        user_input,
        candidate_labels=["end conversation", "continue conversation"],
        hypothesis_template="This statement is about {}."
    )
    label = classification_result['labels'][0]
    return label == "end conversation"

def classify_user_input(user_input):
    classification_result = classifier(
        user_input,
        candidate_labels=["asking_availability_menu", "asking_price", "order_menu", "quantity_order", "giving_address", "cancel_order"],
        hypothesis_template="The user is {}."
    )
    label = classification_result['labels'][0]
    return label
