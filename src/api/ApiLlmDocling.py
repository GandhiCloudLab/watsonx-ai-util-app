from flask import Blueprint, request
import logging, os

from llm_docling.LlmDoclingMain import LlmDoclingMain

apiLlmDocling = Blueprint('api_llm_docling', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@apiLlmDocling.route('/api/docling/invoke', methods=['POST'])
def invoke_docling():
    logger.debug("/api/docling/invoke ...")

    payload = request.get_json()

    ### Call the main function to get the response
    llmDoclingMain = LlmDoclingMain()
    resp = llmDoclingMain.invoke(payload)

    return resp, 200

@apiLlmDocling.route('/api/docling/welcome', methods=['GET'])
def welcome_docling():
    resp = {"msg" : "Welcome to Docling LLM APIs"}
    return resp, 200