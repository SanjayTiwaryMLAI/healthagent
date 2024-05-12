import os
import time
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
import boto3
import logging
import uuid
import botocore
import pprint

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
st.set_page_config(layout="wide")
st.title("👨‍⚕️ Health Agent Demo Powered by AWS Bedrock Agent 🚀")


client = boto3.client('bedrock-agent-runtime',  region_name="us-east-1")

agent_alias_id = os.environ.get('AGENT_ALIAS_ID', 'VGHM588LIX')
agent_id = os.environ.get('AGENT_ID', 'OF1ILSSFEH')
session_id = str(uuid.uuid1())  # random identifier
enable_trace = True
input_text = ""
agent_response = ""

def get_type(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'type':
                return value
            else:
                result = get_type(value)
                if result is not None:
                    return result

def generate_new_session_id():
    new_session_id = str(uuid.uuid4())
    return new_session_id

# Define function to get agent response
@st.cache_data
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
    final_answer = ""
    traces = []

    try:
        for event in event_stream:
            if 'chunk' in event:
                data = event['chunk']['bytes']
                logger.info(f"Final answer ->\n{data.decode('utf8')}")
                final_answer += data.decode('utf8')
            elif 'trace' in event:   
                model_input_type = get_type(event['trace'])
                
                with st.expander(f"{model_input_type}", expanded=False):
                    st.json(event['trace']['trace'])
                        

            else:
                raise Exception("unexpected event.", event)
    except Exception as e:
        raise Exception("unexpected event.", e)


    return final_answer

if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "response" not in st.session_state:
    st.session_state.response = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

for response in st.session_state.response:
    with st.chat_message(response["role"]):
        st.markdown(response["content"])
        
prompt = st.chat_input("How can I help?")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):         
        response = get_agent_response(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})