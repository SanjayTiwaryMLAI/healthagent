import os
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
import boto3
import logging
import uuid
import botocore
import pprint

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Set page title and layout
st.set_page_config(page_title="Agent AWS", layout="wide")

# Create a client instance
client = boto3.client('bedrock-agent-runtime', region_name="us-east-1")

# Initialize session variables
agent_alias_id = os.environ.get('AGENT_ALIAS_ID', 'VGHM588LIX')
agent_id = os.environ.get('AGENT_ID', 'OF1ILSSFEH')
session_id = str(uuid.uuid1())  # random identifier
enable_trace = True
input_text = ""
agent_response = ""

# Define function to get agent response
def get_agent_response(input_text):
    # invoke the agent API
    response = client.invoke_agent(
        inputText=input_text,
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id,
        enableTrace=enable_trace
    )

    logger.info(pprint.pprint(response))

    import json
    event_stream = response['completion']
    try:
        for event in event_stream:
            if 'chunk' in event:
                data = event['chunk']['bytes']
                logger.info(f"Final answer ->\n{data.decode('utf8')}")
                return data.decode('utf8')
            elif 'trace' in event:
                logger.info(json.dumps(event['trace'], indent=2))
            else:
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.", e)

# Streamlit app layout
st.title("Agent AWS")

# Create a container for the chat history
conversation = st.container()

# Create a function to generate the chat message
def generate_message(is_user, text):
    icon = "🙂" if is_user else "🤖"
    message_markdown = f"**{icon}** {text}"
    st.markdown(message_markdown)

# Create the input area for the user
user_input = st.text_input("Enter your message:", key="user_input")
submit_button = st.button("Submit")

# Clear the input area after submitting
if submit_button:
    input_text = user_input
    user_input = ""

    # Generate the user message
    with conversation:
        generate_message(True, input_text)

    # Get the agent response
    agent_response = get_agent_response(input_text)

    # Generate the agent message
    with conversation:
        generate_message(False, agent_response)

# Placeholder for additional controls or information
st.markdown("---")