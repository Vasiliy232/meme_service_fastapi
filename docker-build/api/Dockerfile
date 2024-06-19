FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

ENV PYTHONBUFFERED=1

COPY requirements.txt requirements.txt

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .