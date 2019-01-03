FROM python:3.7-slim

RUN addgroup --system hstorms && adduser --system --ingroup hstorms hstorms

WORKDIR /app
COPY hstorms /hstorms
COPY config /config
COPY requirements.txt ./

RUN pip install -r requirements.txt

ENV DEBUG=false
ENV HSTORMSDB_URI="postgres://hstorms:hstorms@127.0.0.1:5432/hstorms"

EXPOSE 8000
USER hstorms
CMD ["hypercorn", "-c", "python:config/hypercorn.py", "hstorms.app:create_app()"]
