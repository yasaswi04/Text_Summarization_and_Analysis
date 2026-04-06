
'''import os
import sys

import cons

import chromadb

import streamlit as st

from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = cons.APIKEY

st.title('GPT Creator')
prompt = st.text_input('Enter your query here!')

# Check if a prompt is provided
if prompt:
    # Define the directory where your text files are stored
    data_directory = "."

    # Create a VectorstoreLoader based on the data directory
    loader = DirectoryLoader(data_directory, glob="*.txt")

    # Create the VectorstoreIndex using the loader
    index = VectorstoreIndexCreator().from_loaders([loader])

    # Query the index with the user's prompt using ChatOpenAI
    results = index.query(prompt, llm=ChatOpenAI())

    # Display the results
    st.write("Results:")
    for result in results:
        st.write(result)
else:
    st.write("Please enter a query in the input box above.")'''





'''# Define 'ids' as an empty list
ids = []

# Add elements to 'ids' as needed
ids.append(1)
ids.append(2)
ids.append(3)

if len(ids) > 0:
    if isinstance(ids[0], (int, float)):
        import os
        import streamlit as st

        import cons

        from langchain.document_loaders import DirectoryLoader
        from langchain.indexes import VectorstoreIndexCreator

        # Set the OpenAI API key
        os.environ["OPENAI_API_KEY"] = cons.APIKEY

        st.title('GPT Creator')
        prompt = st.text_input('Enter your query here!')

        if prompt:
            # Use Streamlit to input queries

            # Use the DirectoryLoader to load text files in the current directory
            loader = DirectoryLoader(".", glob="*.txt")

            # Check if loader is not empty
            if loader:
                st.write("Indexing documents...")
                # Create a VectorstoreIndex from the loader
                index = VectorstoreIndexCreator().from_loaders([loader])
                st.write("Indexing complete.")

                # Query the index with the user's input
                results = index.query(prompt)

                if results:
                    # Display the results in a Streamlit table
                    st.write("Search results:")
                    st.table(results)

                else:
                    st.write("No results found for the query.")

            else:
                st.write("No documents found for indexing.")

        else:
            st.write("Please enter a query in the input box.")
    else:
        print("IDs are not of the expected type.")
else:
    print("No IDs found in the data.")'''










'''
import os

import cons


from flask import Flask, request, jsonify, render_template

from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

app = Flask(__name__)

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = cons.APIKEY

# Initialize your VectorstoreIndexCreator
loader = DirectoryLoader(".", glob="*.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

@app.route('/')
def home():
    # You can render your HTML template here
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    if request.method == 'POST':
        input_text = request.json.get('text')

        conversation = []

        # Add the user's input to the conversation
        conversation.append({"role": "user", "content": input_text})

        # results = index.query(input_text, llm=ChatOpenAI())
        results = index.query(input_text)

        response = results

        conversation.append({"role": "llm", "content": response})

        return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
'''






import cons

import os
import sqlite3
from flask import Flask, request, jsonify, render_template


from langchain.document_loaders import TextLoader
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = cons.APIKEY

# Initialize your VectorstoreIndexCreator
loader = DirectoryLoader(".", glob="*.txt")
index = VectorstoreIndexCreator().from_loaders([loader])

# Function to create a database connection
def get_db_connection():
    conn = sqlite3.connect('feedback.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to create the "feedback" table
def create_feedback_table():
    with get_db_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                generated_response TEXT NOT NULL,
                feedback_score INTEGER NOT NULL
            )
        ''')
        print("Table 'feedback' created or already exists.")

# Function to log errors
def log_error(exception, message):
    # Log the error details, you can replace this with your preferred logging mechanism
    print(f"Error: {exception}, Message: {message}")

# Endpoint for the default root path
@app.route('/')
def home():
    # You can render your HTML template here
    return render_template('index.html')

# Endpoint for collecting feedback
@app.route('/collect_feedback', methods=['POST'])
def collect_feedback():
    try:
        data = request.get_json()

        # Validate input
        if 'input' not in data or 'response' not in data or 'score' not in data:
            return jsonify({'error': 'Invalid input. Required fields: input, response, score'}), 400

        input_text = data['input']
        generated_response = data['response']
        feedback_score = data['score']

        # Validate score
        if not isinstance(feedback_score, int) or feedback_score not in [-1, 0, 1]:
            return jsonify({'error': 'Invalid score. Score should be -1, 0, or 1'}), 400

        # Store feedback in the database
        with get_db_connection() as conn:
            conn.execute('''
                INSERT INTO feedback (input_text, generated_response, feedback_score)
                VALUES (?, ?, ?)
            ''', (input_text, generated_response, feedback_score))

        return jsonify({'message': 'Feedback collected successfully'})

    except Exception as e:
        log_error(e, "Error collecting feedback")
        return jsonify({'error': 'Internal Server Error'}), 500

# Endpoint for generating a response
@app.route('/generate_response', methods=['POST'])
def generate_response_endpoint():
    try:
        data = request.get_json()

        # Validate input
        if 'text' not in data:
            return jsonify({'error': 'Invalid input. Required field: text'}), 400

        input_text = data['text']

        # Get response from your model
        # Use gpt-3.5-turbo-instruct as the model
        # results = index.query(input_text, llm=ChatOpenAI())
        results = index.query(input_text, llm=ChatOpenAI(model_name="gpt-3.5-turbo"))
        response = results

        # Add the user's input and model's response to the conversation
        conversation = [{"role": "user", "content": input_text}, {"role": "llm", "content": response}]

        return jsonify({'response': response, 'conversation': conversation})

    except Exception as e:
        log_error(e, "Error generating response")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    create_feedback_table()
    app.run(debug=True)