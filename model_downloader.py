import logging
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_and_save_models():
    logging.info("Starting the download and save process for models.")

    # Load the QA model and tokenizer
    logging.info("Loading QA model and tokenizer...")
    qa_model_name = "deepset/roberta-base-squad2-distilled"
    qa_model = AutoModelForQuestionAnswering.from_pretrained(qa_model_name)
    qa_tokenizer = AutoTokenizer.from_pretrained(qa_model_name)
    logging.info("Saving QA model and tokenizer...")
    qa_model.save_pretrained("models/qa")
    qa_tokenizer.save_pretrained("models/qa")
    logging.info("QA model and tokenizer saved successfully.")

    # Load the sentiment analysis model and tokenizer
    logging.info("Loading sentiment analysis model and tokenizer...")
    sentiment_model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    sentiment_model = AutoModelForSequenceClassification.from_pretrained(sentiment_model_name)
    sentiment_tokenizer = AutoTokenizer.from_pretrained(sentiment_model_name)
    logging.info("Saving sentiment analysis model and tokenizer...")
    sentiment_model.save_pretrained("models/sentiment")
    sentiment_tokenizer.save_pretrained("models/sentiment")
    logging.info("Sentiment analysis model and tokenizer saved successfully.")

    # Load the text classification model and tokenizer
    logging.info("Loading text classification model and tokenizer...")
    classifier_model_name = "valhalla/distilbart-mnli-12-3"
    classifier_model = AutoModelForSequenceClassification.from_pretrained(classifier_model_name)
    classifier_tokenizer = AutoTokenizer.from_pretrained(classifier_model_name)
    logging.info("Saving text classification model and tokenizer...")
    classifier_model.save_pretrained("models/classifier")
    classifier_tokenizer.save_pretrained("models/classifier")
    logging.info("Text classification model and tokenizer saved successfully.")

    logging.info("All models downloaded and saved successfully.")

if __name__ == "__main__":
    download_and_save_models()
    logging.info("Process completed.")
