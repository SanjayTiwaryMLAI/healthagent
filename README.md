# Amazon Bedrock Custom LangChain Agent

Create a custom LangChain agent dubbed "Agent AWS" that queries the AWS Well-Architected Framework and deploys Lambda functions, all backed by Amazon Bedrock and housed in a Streamlit chatbot.

<div align="center"><img src="images/agent_aws_pic.png" alt="Agent AWS"></div>

## Prerequisites

Before you begin, make sure you have the following:

* AWS Account: You'll need an AWS account with access to Claude via [Amazon Bedrock](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess).
* Lambda Role: Create an IAM role with Lambda execution permissions.
* S3 Bucket: Create an S3 bucket to store assets like Python deployment zips for Lambda.
* Python 3.9 or higher

Navigate into the project directory:
```bash
cd amazon-bedrock-custom-langchain-agent
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:

```bash
streamlit run agent_aws_st.py
```


Run the Streamlit app:

```bash
source .llmv/bin/activate 
```


