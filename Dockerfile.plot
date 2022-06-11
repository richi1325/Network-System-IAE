FROM python:3.9.13-slim

RUN python -m pip install --upgrade pip

RUN ln -sf /usr/share/zoneinfo/Mexico/BajaNorte /etc/localtime
RUN echo "Mexico/BajaNorte" > /etc/timezone

COPY ["./plot/requirements.txt", "/app/"]

WORKDIR /app

RUN pip install -r requirements.txt

RUN rm requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development 

COPY ["./plot/","."]

EXPOSE 5000

CMD ["flask", "run"]