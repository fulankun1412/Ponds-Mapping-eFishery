FROM python:3.9.16-bullseye

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir app

COPY . /app

WORKDIR /app

RUN pip install --no-deps -r requirements.txt

RUN pip install torch  --extra-index-url https://download.pytorch.org/whl/cpu

# Expose the port to the host
EXPOSE 8501

# configure the container to run in an executed manner
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]