from flask import Blueprint, request
import logging, os

from text_llm.TextLlmMain import TextLlmMain

apiTextLlm = Blueprint('api_text_llm', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@apiTextLlm.route('/api/text/invoke', methods=['POST'])
def text_invoke():
    logger.debug("/api/text/invoke ...")

    payload = request.get_json()

    ### Call the main function to get the response
    textLlmMain = TextLlmMain()
    resp = textLlmMain.invoke(payload)

    return resp, 200

@apiTextLlm.route('/api/text/welcome', methods=['GET'])
def text_welcome():
    resp = {"msg" : "Welcome to Text LLM APIs"}
    return resp, 200