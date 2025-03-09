# Website AI assistant

## Installation

### Prerequisites

- Python 3.x

### Backend Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/nithinv-27/Website_chatbot.git
   ```
   
3. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

4. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

5. Create a file named `keys.env` in the root directory of the project with the following content:

    ```
    GROQ_API_KEY=your-groq-api-key
    BASE_URL=website-base-url
    ```

    - Replace `your-groq-api-key` with your Groq API key.
    - You can visit the Groq Console by clicking the link below and create an api key.
      
      🔗 [Groq API Keys](https://console.groq.com/keys)  

    - Replace `website-base-url` with your Website's Base Url.
      
6. Run the FastAPI backend:

    ```bash
    python ./main.py
    ```
7. Go to the link below to access the site:

    ```bash
    http://localhost:8000/static 
    ```
