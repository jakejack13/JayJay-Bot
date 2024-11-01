FROM python:3.14-rc-slim

COPY . .

RUN python -m pip install --upgrade pip

RUN python -m pip install discord discord.py

CMD ["python","src/JayJay-Programming.py"]