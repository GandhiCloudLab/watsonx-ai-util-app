from flask import Blueprint, request
import logging, os

from llm_image.LlmImageMain import LlmImageMain

apiLlmImage = Blueprint('api_llm_image', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@apiLlmImage.route('/api/image/invoke', methods=['POST'])
def invoke_image():
    logger.debug("/api/image/invoke ...")

    payload = request.get_json()

    ### Call the main function to get the response
    llmImageMain = LlmImageMain()
    resp = llmImageMain.invoke(payload)

    return resp, 200

@apiLlmImage.route('/api/image/welcome', methods=['GET'])
def welcome_image():
    resp = {"msg" : "Welcome to LLM Image APIs"}
    return resp, 200