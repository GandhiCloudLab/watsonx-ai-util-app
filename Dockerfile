FROM python:3.11-slim

WORKDIR /app

COPY ./ /app
RUN pip install -r requirements.txt

ENV LOGLEVEL INFO

ENV TEMP_FOLDER=/app \
    WATSONX_IBMC_AUTH_URL=https://iam.cloud.ibm.com/identity/token \
    WATSONX_CREDENTIALS_URL=https://us-south.ml.cloud.ibm.com \
    WATSONX_API_URL=https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29 \
    WATSONX_API_KEY=xxxxx \
    WATSONX_PROJECT_ID=53302198-522e-49a6-ba45-b445d46db666 \
    WATSONX_MODEL_ID=meta-llama/llama-3-2-90b-vision-instruct \
    WATSONX_MODEL_ID_IMAGE=meta-llama/llama-3-2-90b-vision-instruct \
    WATSONX_MODEL_ID_TEXT=ibm/granite-3-8b-instruct \
    FLASK_ENV=production

EXPOSE 3001

CMD ["python", "-u", "./src/main.py"]