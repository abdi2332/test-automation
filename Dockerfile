FROM mcr.microsoft.com/playwright/python:v1.60.0-jammy

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY test_portal.py .

CMD ["pytest", "test_portal.py", "--html=report.html", "--self-contained-html"]