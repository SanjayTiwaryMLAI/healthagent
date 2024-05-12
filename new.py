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

st.title("Agent AWS")

client = boto3.client('bedrock-agent-runtime',  region_name="us-east-1")

input_text:str = "Hi" 
agent_alias_id = os.environ.get('AGENT_ALIAS_ID', 'VGHM588LIX')
agent_id = os.environ.get('AGENT_ID', 'OF1ILSSFEH')

session_id:str = str(uuid.uuid1()) # random identifier
enable_trace:bool = True


# invoke the agent API
response = client.invoke_agent(inputText=input_text,
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
            end_event_received = True
            # End event indicates that the request finished successfully
        elif 'trace' in event:
            logger.info(json.dumps(event['trace'], indent=2))
        else:
            raise Exception("unexpected event.", event)
except Exception as e:
    raise Exception("unexpected event.", e)