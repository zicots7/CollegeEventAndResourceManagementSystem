FROM python:3.13.5-alpine

WORKDIR /home/app/CollegeEventsAndResourcesManager

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 9001

CMD ["gunicorn", "-b","0.0.0.0:9001","CollegeEventandResourceManagement.wsgi:application"]