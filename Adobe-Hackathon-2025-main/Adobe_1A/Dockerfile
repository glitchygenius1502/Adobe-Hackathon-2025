FROM --platform=linux/amd64 python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir PyMuPDF==1.24.13
COPY process_pdfs.py .
RUN mkdir -p /app/input /app/output
CMD ["python", "process_pdfs.py"]
