import os
import sys
sys.path.append(os.path.join(os.getcwd(), ".python_packages", "lib", "site-packages"))
import re
import json
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from azure.ai.inference.models import SystemMessage, UserMessage
import azure.functions as func
import logging

AZURE_ENDPOINT = "https://DeepSeek-R1-qfags.eastus2.models.ai.azure.com"
AZURE_KEY = "5G4Mb2HfmaFkeKgnuYFnik2CnutqWlqj"

#@app.route(route="llm-call", methods=["POST"])
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
