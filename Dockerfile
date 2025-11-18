FROM python:3.11

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY translate.py .

EXPOSE 7860

CMD ["python3", "translate.py"]
