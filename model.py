import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from langchain.schema import HumanMessage


# Load a sentence transformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Define website base URL
BASE_URL = "https://www.ubayog.com"

# Define intents with sample queries and webpage links
intents = {
    "Listing Items for Sale": {
        "examples": ["I want to list my items", "How do I sell something?", "Post a rental offer"],
        "link": f"{BASE_URL}/sell"
    },
    "Searching for Rentals": {
        "examples": ["Find me a rental", "I need to rent equipment", "Look for available properties"],
        "link": f"{BASE_URL}/rentals"
    },
    "Exploring Services": {
        "examples": ["Find service providers", "I need help with something", "Available services"],
        "link": f"{BASE_URL}/services"
    },
    "Buying & Selling Real Estate": {
        "examples": ["I want to buy a property", "Show me houses for sale", "Find real estate options"],
        "link": f"{BASE_URL}/real-estate"
    },
    "Agricultural & Farming Needs": {
        "examples": ["Find farming tools", "Search agricultural land", "Get farming equipment"],
        "link": f"{BASE_URL}/agriculture"
    },
    "Machinery & Industrial Equipment": {
        "examples": ["Rent a machine", "Buy industrial equipment", "Machinery purchase"],
        "link": f"{BASE_URL}/machinery"
    },
    "Monetizing Skills & Services": {
        "examples": ["Monetize my skills", "Earn with my assets", "Offer my services"],
        "link": f"{BASE_URL}/services"
    },
    "User Account Management": {
        "examples": ["Change my profile details", "Reset my password", "Delete my account"],
        "link": f"{BASE_URL}/account"
    },
    "Referral & Rewards Program": {
        "examples": ["How do I refer a friend?", "Earn rewards by referrals", "Track my referral earnings"],
        "link": f"{BASE_URL}/referrals"
    },
    "General Help & Support": {
        "examples": ["Help me with this site", "Where are the FAQs?", "Contact support"],
        "link": f"{BASE_URL}/help"
    }
}

# Function to classify user query
def classify_intent(query):
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)

    best_intent = None
    max_score = 0
    threshold = 0.6  # Adjust if necessary

    for intent, data in intents.items():
        example_embeddings = embedding_model.encode(data["examples"], convert_to_tensor=True)
        similarity_scores = util.pytorch_cos_sim(query_embedding, example_embeddings).squeeze()
        max_example_score = similarity_scores.max().item()

        if max_example_score > max_score:
            max_score = max_example_score
            best_intent = intent

    return best_intent if max_score >= threshold else None

# Function to generate AI response using LangChain + Groq
def generate_response(intent):
    load_dotenv("keys.env")

    if "GROQ_API_KEY" not in os.environ:
        print("No api keyyyy")
        return None
    
    else:
    
        llm = ChatGroq(model="llama3-8b-8192", temperature=0.1)
        prompt = f"""
        You are an AI chatbot for the website {BASE_URL}. 
        A user has asked a question related to '{intent}'. 
        If user greets then greet the user.
        Provide a concise response and suggest visiting the relevant page for more details.
        """

        response = llm([HumanMessage(content=prompt)])

        return response.content if response else "I'm sorry, but I couldn't generate a response right now."
