# Use an official lightweight Python image as a parent image
FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Create directories for input/output
RUN mkdir -p /app/input /app/output

# 1. Copy only the requirements file first
COPY requirements.txt .

# 2. Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 3. Download required models and NLTK data during build (for offline execution)
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
RUN python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

# 4. Copy the rest of your project files
COPY . .

# 5. Make sure the script is executable
RUN chmod +x process_persona.py

# 6. Command to run the persona analysis script
CMD ["python", "run_challenge_1b.py"]
