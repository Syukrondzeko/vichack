from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# FastAPI initialization
app = FastAPI()

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

# Define greeting mood
class UserMoodRequest(BaseModel):
    user_mood_request: str

# Define data models for ask_menu
class MenuRequest(BaseModel):
    user_menu_request: str

class MenuResponse(BaseModel):
    menu: str

# Define data models for ask_quantity
class QuantityRequest(BaseModel):
    menu: str
    user_quantity_request: str

class QuantityResponse(BaseModel):
    quantity: str

# Define wether user want to add more order or not
class EndChatRequest(BaseModel):
    is_end_chat: str

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

@app.post("/end_chat/")
async def order_summary(chat_request: EndChatRequest):
    global classifier

    load_classifier()

    user_input = chat_request.is_end_chat.strip().lower()
    if check_conversation_end(user_input):
        response = "Thank you for chatting! Have a great day!"
    else:
        response = "What else would you like to order?"

    return {"response": response}

# Helper functions
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
