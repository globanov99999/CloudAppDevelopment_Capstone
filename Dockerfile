FROM python:3.8.2
ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

RUN apt-get update && apt-get install -y apt-utils netcat

ENV APP=/capstone

# Change the workdir.
WORKDIR $APP

# Install the requirements
COPY server/requirements.txt $APP
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the files
COPY . $APP

EXPOSE 8000

COPY entrypoint.sh $APP
RUN chmod +x $APP/entrypoint.sh
ENTRYPOINT [$APP+"/entrypoint.sh"]

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]