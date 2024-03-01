# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure Poetry's bin directory is in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && poetry install

# Expose the port the app runs on
EXPOSE 8501

# Run the Streamlit app
CMD ["poetry", "run", "streamlit", "run", "app3.py"]
