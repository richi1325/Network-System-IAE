FROM python:3.9.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm nmap
RUN ln -sf /usr/share/zoneinfo/Mexico/BajaNorte /etc/localtime
RUN echo "Mexico/BajaNorte" > /etc/timezone

COPY ["./plot/requirements.txt", "/app/"]
COPY ["./plot/package.json", "/app/"]

WORKDIR /app
RUN pip install -r requirements.txt
RUN npm install
RUN npx tailwindcss init -p

COPY ["./plot/","."]

RUN npx tailwindcss -i ./src/tailwind.css -o ./static/css/tailwind.css

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development 

EXPOSE 5000

CMD ["flask", "run"]