FROM python:3

# optional command
WORKDIR /usr/src/app

# copying dependencies
COPY requirements.txt ./

# installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copying everything in our current directory to the current working directory in our container
COPY . .

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]