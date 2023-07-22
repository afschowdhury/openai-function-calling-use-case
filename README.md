
# OpenAI's Function Calling Use Case Demo
<hr>

This repository showcases a practical demonstration of utilizing OpenAI's function calling for complex database queries, thereby minimizing costs typically associated with Langchain's agent and tools.

## Instructions:
<hr>
Follow the steps below to set up and run the demo:

### Clone the Repository:

Clone this repository to your local machine using the following command:


`git clone git@github.com:afschowdhury/openai-function-calling-use-case.git`

### Create a Virtual Environment:

Change into the project directory and create a virtual environment (optional but recommended):


```cd openai-function-calling-demo
python -m venv venv
source venv/bin/activate  
```
### Install Dependencies:

Install the required packages using the provided requirements.txt file:


```pip install -r requirements.txt```

### Run the Demo:

Execute the following command to run the demo application using Chainlit:


```chainlit run app.py -w```

This command will start the application with a chatbot interface in your browser, allowing you to interact with OpenAI's function calling in real-time.
<hr>

*Note:*Please make sure you have obtained the necessary OpenAI API key or access credentials before running the demo.

