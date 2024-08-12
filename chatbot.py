from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

# Load the QA model and tokenizer from the local directory
qa_model_path = "models/qa"
qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_path)
qa_tokenizer = AutoTokenizer.from_pretrained(qa_model_path)

# Create a question-answering pipeline using the local model and tokenizer
qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=qa_tokenizer, framework='pt')

# Load the sentiment analysis pipeline from the local directory
sentiment_model_path = "models/sentiment"
sentiment_pipeline = pipeline("sentiment-analysis", model=sentiment_model_path, framework='pt')

# Load the text classification pipeline for NLI from the local directory
classifier_model_path = "models/classifier"
classifier = pipeline("zero-shot-classification", model=classifier_model_path, framework='pt')

# Define a conversational logic using sentiment analysis
class ConversationalChatbot:
    def __init__(self, qa_pipeline, sentiment_pipeline, classifier):
        self.qa_pipeline = qa_pipeline
        self.sentiment_pipeline = sentiment_pipeline
        self.classifier = classifier
        self.current_step = 0
        self.orders = []

    def initial_greeting(self):
        print("Chatbot: Hey, how is your day?")

    def ask_question(self, context, question):
        result = self.qa_pipeline({
            "context": context,
            "question": question
        })
        return result['answer']

    def determine_sentiment(self, user_input):
        # Use the sentiment analysis pipeline to determine sentiment
        sentiment_result = self.sentiment_pipeline(user_input)
        sentiment = sentiment_result[0]['label'].lower()
        return sentiment

    def generate_response(self, sentiment):
        # Generate a response based on sentiment
        if sentiment == "positive":
            return "Wow, nice to hear that! What do you want to order today?"
        elif sentiment == "negative":
            return "I'm sorry to hear that. Maybe a nice meal can help! What do you want to order?"
        else:
            return "Thanks for sharing. What do you want to order today?"

    def check_conversation_end(self, user_input):
        # Use the classifier to determine if the user wants to end the conversation
        classification_result = self.classifier(
            user_input,
            candidate_labels=["end conversation", "continue conversation"],
            hypothesis_template="This statement is about {}."
        )
        label = classification_result['labels'][0]
        return label == "end conversation"

    def chat(self):
        self.initial_greeting()
        while True:
            user_input = input("You: ").strip().lower()

            if self.current_step == 0:
                # Determine sentiment and respond accordingly
                sentiment = self.determine_sentiment(user_input)
                response = self.generate_response(sentiment)
                print(f"Chatbot: {response}")
                self.current_step += 1

            elif self.current_step == 1:
                # Process user's order and ask for quantity
                menu_item = self.ask_question(user_input, "What menu customer want to order?")
                print(f"Chatbot: Great! How many {menu_item} do you want?")
                self.current_step += 1
                self.orders.append({'menu': menu_item, 'quantity': None})

            elif self.current_step == 2:
                # Extract quantity and update order
                quantity = self.ask_question(user_input, "What is the quantity?")
                self.orders[-1]['quantity'] = quantity
                print(f"Chatbot: You have ordered {quantity} of {self.orders[-1]['menu']}.")
                print("Chatbot: Is there anything else you need?")
                self.current_step += 1

            else:
                # Use LLM to determine if the conversation should end
                if self.check_conversation_end(user_input):
                    print("Chatbot: Thank you for chatting! Have a great day!")
                    break
                else:
                    print("Chatbot: What else would you like to order?")
                    self.current_step = 1

        return self.orders

# Initialize and start the chatbot
if __name__ == "__main__":
    chatbot = ConversationalChatbot(qa_pipeline, sentiment_pipeline, classifier)
    orders = chatbot.chat()
    print("\nFinal Orders:")
    for order in orders:
        print(order)
