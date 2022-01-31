FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data
COPY main.py .
COPY database-tools.py .
COPY worker/* .

CMD [ "/bin/bash", "entrypoint.sh"]