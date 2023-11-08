FROM python:3.13.0a1
LABEL authors="nicholasball"

EXPOSE 5000
ENV PORT 5000

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3","app.py"]