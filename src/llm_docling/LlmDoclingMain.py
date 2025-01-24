import os, json, logging

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from docling.document_converter import DocumentConverter

from util.FileUtil import FileUtil

from llm.LlmMain import LlmMain

from CommonConstants import *

class LlmDoclingMain(object):

    def __init__(
        self
    ) -> None:
        load_dotenv()
        self._init_config()

    def _init_config(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())
        self.converter = DocumentConverter()
        self.fileUtil = FileUtil()
        self.fileUtil.start()

    def invoke(self, payload):
        self.logger.info("invoke started ... ")
        
        ### file_url
        file_url = payload["file_url"]

        ### download file
        file_name = self.fileUtil.download_file(file_url)

        ### Call docling to extract the pdf content
        file_content = self.extract_data_from_pdf (file_name)

        ### Prompt
        prompt = self.get_prompt(file_content)

        ### Get watsonx model
        llmMain = LlmMain()
        model = llmMain.get_watsonx_model_for_utility_bills_docling()

        ### call watsonx model
        json_data = llmMain.callWatsonx_for_utility_bills_docling(model, prompt)

        ### Write it in output file
        self.fileUtil.writeInFileWithCounter("output-docling.json", json.dumps(json_data))

        ### result
        resp = {
            "msg" : "Success",
            "result" : json_data
        }
        self.logger.info("invoke completed ... ")
        return resp


    def extract_data_from_pdf(self, pdf_file_name):
        result = self.converter.convert(pdf_file_name)
        markdown_output =  result.document.export_to_markdown()
        return markdown_output

    def get_prompt(self, file_content) :
        prompt_template = PromptTemplate(
            input_variables=["DOCUMENT"],
            template='''
            <|start_of_role|>System<|end_of_role|> You are an AI assistant for processing invoices. Based on the provided invoice data, extract the 'Invoice Number', 'Total Net Amount', 'Total VAT or TAX or GST Amount', 'Total Amount' , 'Invoice Date', 'Purchase Order Number' and 'Customer number', without the currency values.

            |Instructions|
            Identify and extract the following information:
            - **Invoice Number**: The unique identifier for the invoice.
            - **Supplier Name**: The organization name, who created this invoice.
            - **Net Amount**: The Total Net Amount indicated on the invoice.
            - **VAT or TAX or GST Amount**: The Total VAT or TAX or GST Amount indicated on the invoice.
            - **Total Amount**: The Total Cost indicated on the invoice.
            - **Invoice Date**: The date the invoice was issued.
            - **Invoice Start Date**: The date the invoice period starts.
            - **Invoice End Date**: The date the invoice period ends.
            - **Customer Number**: The unique identifier for the customer.
            - **Customer Name**: The name of the customer.
            - **Item Description: The item description available in the invoice.
            - **Total Quantity: The total quantity in the invoice.

            Invoice Data:
            {DOCUMENT}


            Strictly provide the extracted information in the following JSON format:

            ```json
            {{
            "invoice_number": "extracted_invoice_number",
            "supplier_name": "extracted_supplier_name",
            "net_amount": "extracted_new_amount",
            "vat_or_tax_or_gst_amount" : "extracted_vat_or_tax_or_gst_amount",
            "total_amount": "extracted_total_amount",
            "invoice_date": "extracted_invoice_date",
            "invoice_start_date": "extracted_invoice_start_date",
            "invoice_end_date": "extracted_invoice_end_date",
            "customer_number": "extracted_customer_number",
            "customer_name": "extracted_customer_name",
            "item_description": "extracted_item_description",
            "total_qty": "extracted_total_quantity"

            }}

            <|end_of_text|>

            <|start_of_role|>assistant<|end_of_role|>
        ''')


        prompt = prompt_template.format(DOCUMENT=str(file_content).strip())

        return prompt
    