FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY download_model.py .
RUN python download_model.py
COPY src/ src/
COPY Collection_* Collection_*/
CMD ["python", "src/main.py"]