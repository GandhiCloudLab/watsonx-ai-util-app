import os
import base64
import json
import os
import requests
import wget
from dotenv import load_dotenv
import logging 
import re

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_cloud_sdk_core import IAMTokenManager
from langchain_ibm import WatsonxLLM
import time

from util.FileUtil import FileUtil

class LlmMain(object):

    def __init__(
        self,
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self.TEMP_FOLDER = os.environ.get('TEMP_FOLDER', '')
        self.WATSONX_IBMC_AUTH_URL = os.getenv("WATSONX_IBMC_AUTH_URL", "")
        self.WATSONX_CREDENTIALS_URL = os.getenv("WATSONX_CREDENTIALS_URL", "")
        self.WATSONX_API_URL = os.getenv("WATSONX_API_URL", "")
        self.WATSONX_API_KEY = os.getenv("WATSONX_API_KEY", "")
        self.WATSONX_MODEL_ID_DOCLING = os.getenv("WATSONX_MODEL_ID_DOCLING", "")
        self.WATSONX_MODEL_ID_IMAGE = os.getenv("WATSONX_MODEL_ID_IMAGE", "")
        self.WATSONX_MODEL_ID_TEXT = os.getenv("WATSONX_MODEL_ID_TEXT", "")
        self.WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")
        self.fileUtil = FileUtil()
        self.fileUtil.start()

    def get_watsonx_image_model(self):
        self.logger.info("get_watsonx_image_model Started ")

        self.logger.debug(f"WATSONX_CREDENTIALS_URL : {self.WATSONX_CREDENTIALS_URL} ")
        self.logger.debug(f"WATSONX_PROJECT_ID : {self.WATSONX_PROJECT_ID} ")
        self.logger.debug(f"WATSONX_MODEL_ID : {self.WATSONX_MODEL_ID_IMAGE} ")

        credentials = Credentials(
            url = self.WATSONX_CREDENTIALS_URL,
            api_key = self.WATSONX_API_KEY,
        )
        my_params = TextChatParameters(
            temperature=1
        )
        model = ModelInference(
            model_id = self.WATSONX_MODEL_ID_IMAGE,
            credentials = credentials,
            project_id =  self.WATSONX_PROJECT_ID,
            params = my_params
        )

        self.logger.info("get_watsonx_image_model Completed")

        return model

    def invokeWatsonx_image_model(self, model, file_url, prompt_text):
        self.logger.info("------------------------------------------------ invokeWatsonx_image_model Started ------------------------------------------------")

        ### download file
        file_name_with_path = self.fileUtil.download_file(file_url)

        ### Create base64 file
        with open(file_name_with_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        ### Prompt
        messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_text
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": "data:image/jpeg;base64," + encoded_string,
                    }
                }
            ]
        }
        ]

        ### call watsonx
        response = model.chat(messages=messages)

        ### parse the result
        try:
            result = response["choices"][0]["message"]["content"]
        except Exception as e:
             result = ""

        self.logger.info(f" ----------------------------------")        
        self.logger.info(f" File Name : {file_url}")
        self.logger.info(f" Prompt Text  : {prompt_text}")
        self.logger.info(f" Result    : {result} ")
        self.logger.info(f" ----------------------------------")        

        self.logger.debug(f"------------------------------------------------ invokeWatsonx_image_model Completed ------------------------------------------------")

        return result
    

    def invokeWatsonx_Text_model(self, prompt_text):
        self.logger.info("------------------------------------------------ invokeWatsonx_Text_model Started ------------------------------------------------")

        access_token = IAMTokenManager(apikey = self.WATSONX_API_KEY, url =  self.WATSONX_IBMC_AUTH_URL).get_token()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer '+ access_token
            }
        
        parameters = {
            "decoding_method": "greedy",
            "max_new_tokens": 200,
            "min_new_tokens": 1,
            "repetition_penalty": 1
            }
        
        llmPayload = {
            "project_id": self.WATSONX_PROJECT_ID,
            "model_id": self.WATSONX_MODEL_ID_TEXT, 
            "parameters": parameters,
            "input": prompt_text
            }
        
        ### call watsonx
        llmResponse = requests.post(self.WATSONX_API_URL, json=llmPayload, headers=headers)

        ### parse the result
        result = ""
        try:
            if llmResponse.status_code == 200:
                result = llmResponse.json()["results"][0]["generated_text"]
        except Exception as e:
             result = ""

        self.logger.info(f" ----------------------------------")        
        self.logger.info(f" Prompt Text  : {prompt_text}")
        self.logger.info(f" Result    : {result} ")
        self.logger.info(f" ----------------------------------")   

        self.logger.debug("------------------------------------------------ invokeWatsonx_Text_model Completed ------------------------------------------------")

        return result
    

    def get_watsonx_model_for_utility_bills_docling(self):
        self.logger.info("------------------------------------------------ get_watsonx_model_for_utility_bills_docling Started ------------------------------------------------")
        start_time = time.time()

        llm = WatsonxLLM(
            model_id = self.WATSONX_MODEL_ID_DOCLING,
            apikey=self.WATSONX_API_KEY,
            project_id=self.WATSONX_PROJECT_ID,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 8000,
                "min_new_tokens": 1,
                "repetition_penalty": 1.01
            },
            url=self.WATSONX_CREDENTIALS_URL
        )

        end_time = time.time()
        execution_time = end_time - start_time
        self.logger.info(f"\nExecution time: get_watsonx_model_for_utility_bills : {execution_time} seconds")
        self.logger.debug("------------------------------------------------ get_watsonx_model_for_utility_bills_docling Completed ------------------------------------------------\n\n\n")

        return llm


    def callWatsonx_for_utility_bills_docling(self, llm, prompt):
        self.logger.info("------------------------------------------------ callWatsonx_for_utility_bills_docling Started ------------------------------------------------")
        start_time = time.time()

        answer = llm.invoke(prompt)

        json_string = re.search(r'\{.*\}', answer, re.DOTALL).group(0).replace('\n', '')
        json_data = json.loads(json_string)

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("json_converted.json", json_string)

        end_time = time.time()
        execution_time = end_time - start_time
        self.logger.info(f"\nExecution time: callWatsonx_for_utility_bills_docling : {execution_time} seconds")
        self.logger.debug("------------------------------------------------ callWatsonx_for_utility_bills_docling Completed ------------------------------------------------\n\n\n")

        return json_data    