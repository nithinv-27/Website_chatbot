import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util
from langchain.schema import HumanMessage
import random



# Load a sentence transformer model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

# Define website base URL
BASE_URL = "https://www.ubayog.com"

# Define intents with sample queries and webpage links
intents = {
    "Listing Items for Sale": {
        "examples": [
            "I want to list my items for sale", 
            "How can I sell something here?",
            "Post a rental offer",
            "Where do I add my product listing?",
            "Sell my used equipment",
            "Put an item up for sale",
            "How to advertise my product?",
            "List an item in the marketplace"
        ],
        "response": "To list an item for sale, visit our <a href='{BASE_URL}/sell'>listing page</a>. Fill in the item details and submit. You can also manage your existing listings from your account.",
        "link": "{BASE_URL}/sell",
        "related_keywords": ["sell product", "post a listing", "marketplace", "advertise item", "list my assets"]
    },
    "Searching for Rentals": {
        "examples": [
            "Find me a rental",
            "I need to rent equipment",
            "Look for available properties",
            "Find short-term rentals",
            "Where can I lease equipment?",
            "Search for rental options",
            "Available items for rent",
            "Check rental listings"
        ],
        "response": "You can explore rental listings <a href='{BASE_URL}/rentals'>here</a>. Use filters to narrow down your search based on category, location, and price.",
        "link": "{BASE_URL}/rentals",
        "related_keywords": ["lease", "renting", "short-term rental", "rental marketplace", "rental search"]
    },
    "Exploring Services": {
        "examples": [
            "Find service providers",
            "I need help with something",
            "Show me available services",
            "Hire professionals for my task",
            "Where can I find a freelancer?",
            "Look for skilled workers",
            "Who can provide this service?",
            "Book a service provider"
        ],
        "response": "Browse through various service providers <a href='{BASE_URL}/services'>here</a>. You can filter by category and directly contact professionals.",
        "link": "{BASE_URL}/services",
        "related_keywords": ["hire professional", "book service", "find experts", "outsource task", "freelancer search"]
    },
    "Buying & Selling Real Estate": {
        "examples": [
            "I want to buy a property",
            "Show me houses for sale",
            "Find real estate options",
            "Where can I list my house?",
            "Search for apartments",
            "Real estate investment opportunities",
            "Sell my home quickly",
            "Find commercial property for sale"
        ],
        "response": "Check out the latest real estate listings <a href='{BASE_URL}/real-estate'>here</a>. You can list your own property or find available options to buy.",
        "link": "{BASE_URL}/real-estate",
        "related_keywords": ["property sale", "house listings", "apartment search", "land purchase", "commercial real estate"]
    },
    "Agricultural & Farming Needs": {
        "examples": [
            "Find farming tools",
            "Search for agricultural land",
            "Get farming equipment",
            "Where can I buy seeds and fertilizers?",
            "Rent agricultural machinery",
            "Sell my farm products",
            "Look for farming solutions",
            "Agricultural marketplace"
        ],
        "response": "Explore agricultural tools and land listings <a href='{BASE_URL}/agriculture'>here</a>. You can buy, rent, or sell agricultural products and services.",
        "link": "{BASE_URL}/agriculture",
        "related_keywords": ["farm tools", "agriculture rental", "sell crops", "buy fertilizers", "farm equipment"]
    },
    "Machinery & Industrial Equipment": {
        "examples": [
            "Rent a machine",
            "Buy industrial equipment",
            "Find heavy machinery for sale",
            "Where can I get construction tools?",
            "Sell industrial machinery",
            "Lease factory equipment",
            "Search for mechanical tools",
            "Purchase engineering equipment"
        ],
        "response": "You can find industrial and machinery equipment <a href='{BASE_URL}/machinery'>here</a>. Browse listings or post your own equipment for sale or rent.",
        "link": "{BASE_URL}/machinery",
        "related_keywords": ["construction tools", "engineering machines", "factory equipment", "industrial rental", "heavy-duty tools"]
    },
    "Monetizing Skills & Services": {
        "examples": [
            "Monetize my skills",
            "Earn money with my expertise",
            "Offer my services for hire",
            "How can I freelance here?",
            "List my services for people to hire",
            "Provide consultation",
            "Sell my skills online",
            "Become a service provider"
        ],
        "response": "You can offer your services by listing them <a href='{BASE_URL}/services'>here</a>. Potential clients can find and hire you.",
        "link": "{BASE_URL}/services",
        "related_keywords": ["freelance", "gig work", "skill monetization", "sell services", "consultation jobs"]
    },
    "User Account Management": {
        "examples": [
            "Change my profile details",
            "Reset my password",
            "Delete my account",
            "Update my email address",
            "Modify personal settings",
            "Where can I update my profile?",
            "Change my account preferences",
            "Recover my lost password"
        ],
        "response": "Manage your account settings <a href='{BASE_URL}/account'>here</a>. You can update details, reset your password, or deactivate your account.",
        "link": "{BASE_URL}/account",
        "related_keywords": ["profile settings", "account modification", "password recovery", "delete user", "update email"]
    },
    "Referral & Rewards Program": {
        "examples": [
            "How do I refer a friend?",
            "Earn rewards by referrals",
            "Track my referral earnings",
            "How does the rewards system work?",
            "Get referral bonus",
            "Invite friends for discounts",
            "Explain the referral program",
            "Redeem my referral rewards"
        ],
        "response": "Join our referral program <a href='{BASE_URL}/referrals'>here</a>. Earn rewards for inviting friends and track your referral bonuses.",
        "link": "{BASE_URL}/referrals",
        "related_keywords": ["referral bonus", "earn rewards", "invite & earn", "referral system", "track referral earnings"]
    },
    "General Help & Support": {
        "examples": [
            "Help me with this site",
            "Where are the FAQs?",
            "Contact customer support",
            "I need assistance with my account",
            "Live chat support",
            "Submit a complaint",
            "Where can I find help?",
            "Support team contact"
        ],
        "response": "For any assistance, visit our <a href='{BASE_URL}/help'>Help Center</a>. You can also contact customer support for further inquiries.",
        "link": "{BASE_URL}/help",
        "related_keywords": ["customer service", "support request", "site help", "FAQ section", "technical support"]
    }
}

# Predefined greetings and goodbyes
GREETING_EXAMPLES = [
    "hello", "hi", "hey", "greetings", "good morning", "good afternoon", 
    "good evening", "how are you?", "how do you do?", "what's up?", "yo", "howdy"
]

GOODBYE_EXAMPLES = [
    "bye", "goodbye", "see you", "take care", "farewell", "catch you later", 
    "I'm leaving", "talk to you soon"
]

# Randomized friendly responses
GREETING_RESPONSES = [
    "Hey there! How can I help you today? 😊",
    "Hello! What brings you here today? 👋",
    "Hi! How can I assist you today?",
    "Hey! Hope you're doing great. Need any help?",
    "Greetings! Let me know how I can be of service."
]

GOODBYE_RESPONSES = [
    "Goodbye! Have an amazing day! 👋",
    "See you soon! Take care. 😊",
    "Bye! It was great chatting with you.",
    "Farewell! Reach out if you need anything.",
    "Catch you later! Have a fantastic day!"
]

def classify_intent(query, intents=intents):
    """Classifies the user's query by performing semantic search on intent examples."""
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

def detect_greeting_or_goodbye(user_query):
    """Performs semantic search to detect if the query is a greeting or a goodbye."""
    user_embedding = embedding_model.encode(user_query, convert_to_tensor=True)

    # Compute similarity for greetings
    greeting_embeddings = embedding_model.encode(GREETING_EXAMPLES, convert_to_tensor=True)
    greeting_scores = util.pytorch_cos_sim(user_embedding, greeting_embeddings).squeeze()
    if greeting_scores.max().item() >= 0.7:  # Adjust threshold as needed
        return random.choice(GREETING_RESPONSES)

    # Compute similarity for goodbyes
    goodbye_embeddings = embedding_model.encode(GOODBYE_EXAMPLES, convert_to_tensor=True)
    goodbye_scores = util.pytorch_cos_sim(user_embedding, goodbye_embeddings).squeeze()
    if goodbye_scores.max().item() >= 0.7:
        return random.choice(GOODBYE_RESPONSES)

    return None  # If neither greeting nor goodbye is detected

def generate_response(user_query, intents=intents, BASE_URL=BASE_URL):
    """Generates a response based on greetings, intent classification, and LLM generation."""
    load_dotenv("keys.env")

    if "GROQ_API_KEY" not in os.environ:
        print("Missing API Key")
        return "I'm sorry, but I can't generate a response right now."

    # Check for greetings or goodbyes using semantic search
    greeting_or_goodbye = detect_greeting_or_goodbye(user_query)
    if greeting_or_goodbye:
        response_data = {
        "content": greeting_or_goodbye,
    }
        return response_data # Return friendly greeting or goodbye

    # Classify intent using semantic search
    intent = classify_intent(user_query, intents)

    # If no intent is detected, return a generic help message
    if not intent:
        response_data = {
        "content": "I'm not sure I understand. Could you clarify what you need help with? 😊",
    }
        return response_data

    # Fetch predefined response and link
    # intent_data = intents.get(intent, {})
    # predefined_response = intent_data.get("response", "I'm not sure how to help with that.")

    # Initialize LLM
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.1)

    response_template = intents.get(intent, {}).get("response", "")
    link = intents.get(intent, {}).get("link", "")

    # Replace {BASE_URL} with actual URL if link exists
    link = intents.get(intent, {}).get("link", "")
    link = link.replace("{BASE_URL}", BASE_URL) if link else None

    # Construct prompt for LLM
    prompt = f"""
    You are an AI chatbot for the website {BASE_URL}. 
    A user has asked a question related to '{intent}'. 

    You are not allowed to start with a greeting. Generate a **friendly, engaging, and natural-sounding response** similar in style to the following example:

    ------
    "{response_template}"
    ------

    ### **Response Guidelines:**
    - **Do not start with a greeting.**
    - **Ensure a natural, conversational tone.**
    - **Keep it concise yet engaging.**
    - **Do not include any links in the response.**
    - **Encourage the user to ask questions if they need help.**

    Now, generate the response following these guidelines.
    """

    response = llm([HumanMessage(content=prompt)])

    print(intent)

    # Prepare structured output
    response_data = {
        "content": response.content if response else "I'm sorry, but I couldn't generate a response right now.",
        "link": link,  # Correct BASE_URL replacement
        "intent": intent  # Include the intent name in the response
    }

    return response_data