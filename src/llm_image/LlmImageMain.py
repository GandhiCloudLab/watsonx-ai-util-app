import os
import logging
from xml.dom.minidom import Document 
from dotenv import load_dotenv

import logging 
import os

from llm.LlmMain import LlmMain

from CommonConstants import *

class LlmImageMain(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

    def invoke(self, payload):
        self.logger.info("invoke started ... ")
        
        ### Retrive parameters
        image_url = payload["image_url"]
        question = payload["question"]

        ### Get watsonx model
        llmMain = LlmMain()
        model = llmMain.get_watsonx_image_model()

        ### query watsonx model
        result = llmMain.invokeWatsonx_image_model (model, image_url, question)
        resp = {
            "msg" : "Success",
            "result" : result
        }

        self.logger.info("invoke completed ... ")

        return resp