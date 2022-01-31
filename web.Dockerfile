FROM python:3

WORKDIR /usr/src/app
EXPOSE 8000
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY main.py .
COPY database-tools.py .
COPY entrypoint.sh .

CMD [ "/bin/bash", "entrypoint.sh"]