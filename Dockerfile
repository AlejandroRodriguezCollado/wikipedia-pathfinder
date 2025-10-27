# Imagen base: Python 3.12 slim
FROM python:3.12-slim

# Variables de entorno para que Streamlit no intente abrir navegador y corra en producción
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

WORKDIR /app

# Copia requirements y la app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
