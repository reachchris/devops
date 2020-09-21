FROM python:alpine3.8
COPY code/ /app/
WORKDIR /app
RUN pip install -r requirements.txt 
EXPOSE 5001 
ENTRYPOINT [ "python" ] 
CMD [ "deploy.py" ] 
