FROM python:3.8-alpine
ENV PATH "/opt/venv/bin:$PATH"
RUN apk add \
    openssh \
    git \
    linux-headers \
    alpine-sdk \
    libffi-dev
COPY code/ /app/
WORKDIR /app
RUN pip install -r requirements.txt 
EXPOSE 5001 
ENTRYPOINT [ "python" ] 
CMD [ "deploy.py" ] 
