# Use an official Python runtime as a parent image
FROM --platform=linux/amd64 python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
# Ensure Poetry's bin directory is in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies required for Google Chrome and wget
RUN apt-get update && apt-get install -y wget gnupg2 software-properties-common

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN apt-get update -qqy --no-install-recommends && apt-get install -qqy --no-install-recommends google-chrome-stable


ENV CHROMEDRIVER_VERSION 2.19
ENV CHROMEDRIVER_DIR /chromedriver
RUN mkdir $CHROMEDRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROMEDRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip"
RUN unzip $CHROMEDRIVER_DIR/chromedriver* -d $CHROMEDRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROMEDRIVER_DIR:$PATH

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install

# Expose the port the app runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["poetry", "run", "streamlit", "run", "app3.py"]
