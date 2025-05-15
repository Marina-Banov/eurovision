FROM python:3.9-alpine
WORKDIR /eurovision
RUN pip install flask python-dotenv flask-sqlalchemy flask-migrate flask-cors
COPY . .
RUN mv .env.example .env
RUN flask db upgrade
RUN flask seed
ENV PORT=5000
EXPOSE 5000
CMD [ "flask", "run", "--host", "0.0.0.0" ]
