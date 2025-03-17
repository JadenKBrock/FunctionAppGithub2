import os
import re
import json
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from azure.ai.inference.models import SystemMessage, UserMessage
import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

AZURE_ENDPOINT = "https://DeepSeek-R1-qfags.eastus2.models.ai.azure.com"
AZURE_KEY = "5G4Mb2HfmaFkeKgnuYFnik2CnutqWlqj"


@app.route(route="llm-call", methods=["POST"])
def getLLMResponse(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')


    try:
        req_body = req.get_json()
        content_type = req_body.get("content_type", "")
        content_text = req_body.get("content_text", "")

        if not content_text:
            return func.HttpResponse(
                json.dumps({"error": "Missing 'content_text' in request body."}),
                status_code=400,
                mimetype="application/json"
            )

        client = ChatCompletionsClient(
            endpoint=AZURE_ENDPOINT,
            credential=AzureKeyCredential(AZURE_KEY)
        )

        MAX_CHARACTERS = "63206"

        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content=f"Summarize the following article(s) and convert it into a social media post for Facebook. \
                    Your task is to read the given article(s), extract key insights, and generate a compelling human-like social media post \
                    intended for Facebook - note, the summary is intended to help you get your key ideas out. \
                    Make the post sound like a social media post and not simply just a summary of the article(s). \
                    Keep in mind that the character limit of a Facebook post is {MAX_CHARACTERS} - and that is the MAX, \
                    you don't need to necessarily go to or near that limit.\nArticle: {content_text}"),
            ],
        )

        cleaned_response = re.sub(r'<think>.*?</think>', '', response.choices[0].message.content, flags=re.DOTALL).strip()

        return func.HttpResponse(
            json.dumps({"response": cleaned_response}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )    