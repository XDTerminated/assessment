# Function Calling with Gemini LLM

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project directory and add your API key:

```
GEMINI_API_KEY=your-api-key-here
```

5. Run the script:

```bash
python function_caller.py
```

## Usage

Ask questions about product details and the AI will automatically call the appropriate function to get information.

Example queries:

-   "What is the price of the phone?"
-   "How much RAM does it have?"
-   "Tell me about the specifications"

Type 'quit' to exit.

## How It Works

The script defines a function schema that tells Gemini what the `get_product_details()` function does and when to use it. When you ask a question, Gemini analyzes your query to determine if it needs product information. If so, it calls the function to retrieve mock product data, then uses that data to provide targeted answers based on what you actually asked for (e.g., just the price instead of all details).
