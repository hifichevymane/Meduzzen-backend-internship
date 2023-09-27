FROM python:3.11.3-alpine

# https://stackoverflow.com/questions/59812009/what-is-the-use-of-pythonunbuffered-in-docker-file
ENV PYTHONBUFFERED=1

# https://stackoverflow.com/questions/30494050/how-do-i-pass-environment-variables-to-docker-containers

WORKDIR /code

COPY requirements.txt .

RUN pip install -r requirements.txt --upgrade

COPY . .

# Copy start.sh script into project folder
COPY start.sh .

# Give access rights to start.sh
RUN chmod +x start.sh

# Run the script
ENTRYPOINT [ "./start.sh" ]
