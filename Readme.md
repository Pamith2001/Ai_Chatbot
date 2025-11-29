# 🛒 AI-Powered E-Commerce Chatbot (Pamith Tech Solutions)

This is a full-stack chatbot application designed for an e-commerce platform. It utilizes **Google Gemini 2.5 Flash** to provide intelligent, context-aware responses regarding order status, return policies, and product recommendations.

The project consists of a **React (TypeScript)** frontend and a **Python (Flask)** backend.

---

## 🚀 Tech Stack

- **Frontend:** React, TypeScript, Tailwind CSS, Lucide React
- **Backend:** Python, Flask, Flask-CORS
- **AI Model:** Google Gemini API (gemini-2.5-flash)
- **Data Source:** JSON-based external data loader (`data.json`)

---

## 🛠️ Installation & Setup

Follow these steps to set up and run the project locally.

### 1. Backend Setup (Python)

The backend handles API requests and communicates with the Google Gemini AI.

1.  **Navigate to the project folder.**
2.  **Create and activate a virtual environment:**

    ```bash
    # Create virtual environment (if not already created)
    python -m venv .venv

    # Activate virtual environment (Windows)
    .venv\Scripts\activate
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install google-genai
    pip install python-dotenv
    pip install flask
    pip install flask-cors
    ```

4.  **Configure Environment Variables:**
    * Create a file named `.env` in the same directory as `api.py`.
    * Add your Google Gemini API Key:
        ```env
        GEMINI_API_KEY=your_actual_api_key_here
        ```

5.  **Run the Backend Server:**

    ```bash
    python api.py
    ```
    *The server will start at `http://localhost:8000`*

---

### 2. Frontend Setup (React)

The frontend provides the chat interface for users.

1.  **Open a new terminal** (keep the backend terminal running).
2.  **Install Node dependencies:**

    ```bash
    npm install
    ```

3.  **Run the Development Server:**

    ```bash
    npm run dev
    ```

4.  Open your browser and navigate to the link provided (usually `http://localhost:5173` or `http://localhost:3000`).

---

## 📂 Project Structure

```text
├── api.py           # Main Flask backend server
├── data.json        # External data (Orders, FAQ, Products)
├── .env             # API Key configuration (Not uploaded to git)
├── src/
│   ├── App.tsx      # Main React Chat Component
│   └── main.tsx     # Entry point
└── README.md        # Project documentation