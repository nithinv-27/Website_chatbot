# ubayog_chatbot

## Installation

### Prerequisites

- Python 3.x
- FastAPI and related dependencies

### Backend Setup

1. Clone the repository:

2. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a file named `keys.env` in the root directory of the project with the following content:

    ```
    GROQ_API_KEY=your-groq-api-key
    ```

    - Replace `your-groq-api-key` with your Groq API key.

5. Run the FastAPI backend:

    ```bash
    uvicorn main:app --reload
    ```
    
6. Open the `index.html` in your browser or use a simple server like `live-server` to view the application.
