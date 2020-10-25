FROM python:3.7-alpine
WORKDIR /app
COPY app.py /app
COPY api.py /app
COPY requirements.txt /app/
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5001
RUN pip install -r requirements.txt
EXPOSE 5001/tcp
CMD ["flask", "run"]
