from flask import Blueprint, request
import logging, os

from image_llm.ImageLlmMain import ImageLlmMain

apiImageLlm = Blueprint('api_image_llm', __name__)

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

@apiImageLlm.route('/api/image/invoke', methods=['POST'])
def image_invoke():
    logger.debug("/api/image/invoke ...")

    payload = request.get_json()

    ### Call the main function to get the response
    imageLlmMain = ImageLlmMain()
    resp = imageLlmMain.invoke(payload)

    return resp, 200

@apiImageLlm.route('/api/image/welcome', methods=['GET'])
def image_welcome():
    resp = {"msg" : "Welcome to Image LLM APIs"}
    return resp, 200