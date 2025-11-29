import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
from flask import Flask, request, jsonify 
from flask_cors import CORS 

# --- 1. Configuration & API Key ---
load_dotenv() 
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY not found. Please set it in your .env file.") 

# --- 2. Flask Setup ---
app = Flask(__name__)
# Allow requests from any origin (simplify for development)
CORS(app, resources={r"/*": {"origins": "*"}})

# --- 3. Load External Data from JSON File ---
def load_external_data():
    """Loads data from the data.json file."""
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: data.json file not found!")
        return {} # Return empty dict if file missing
    except json.JSONDecodeError:
        print("ERROR: data.json is not valid JSON!")
        return {}

# Load data when the app starts
EXTERNAL_DATA = load_external_data()

# --- 4. LLM API Call Function (Google GenAI) ---

def llm_api_call(client, user_message, history, external_info):
    """
    Function to call the Google GenAI API for a detailed, context-aware response.
    """
    
    system_prompt = f"""
    You are an AI-powered, helpful, and polite customer support chatbot for an E-commerce platform.
    Your main responsibilities are: answering order status, return policy, and product recommendation questions.
    Shop Name: Pamith Tech Silutions.
    Shop URL: www.pamithtech.com.
    Shop Location: Baddegama.
    
    CRITICAL INSTRUCTION: Use the following EXTERNAL_DATA to answer factual questions. 
    You must intelligently parse the user's request (e.g., find an order ID like ORD123, or a keyword like 'return policy') 
    and provide the specific information found in this JSON object:
    
    EXTERNAL_DATA:
    {json.dumps(external_info, indent=2)}
    
    If you are greeting the user or responding to a general phrase like 'how are you', respond conversationally.
    If you cannot find the answer in the provided data, politely state that you cannot assist with that specific query.
    """

    # Build the conversation content
    contents = [
        types.Content(
            role="user", 
            parts=[types.Part.from_text(text=system_prompt)]
        )
    ]
    
    for message in history:
        contents.append(
            types.Content(
                role=message["role"],
                parts=[types.Part.from_text(text=message["content"])] 
            )
        )
        
    contents.append(
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_message)] 
        )
    )

    try:
        client = genai.Client()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
        )
        return response.text
        
    except Exception as e:
        print(f"An error occurred during the API call: {e}") 
        return "I apologize, but I am experiencing a temporary technical issue with my AI core. Please try again in a moment."

# --- 5. Flask Endpoint ---

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json()
    
    if not data or 'user_message' not in data or 'history' not in data:
        return jsonify({"error": "Missing 'user_message' or 'history' in request body"}), 400

    user_message = data.get('user_message')
    history = data.get('history', [])
    
    # Reload data optionally here if you want real-time updates without restarting server
    # EXTERNAL_DATA = load_external_data() 
    
    client = genai.Client()
    response_text = llm_api_call(
        client=client,
        user_message=user_message,
        history=history,
        external_info=EXTERNAL_DATA
    )
    
    return jsonify({"response": response_text.strip()})

# --- 6. Run the App ---
if __name__ == "__main__":
    app.run(debug=True, port=8000)