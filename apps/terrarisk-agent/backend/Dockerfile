FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip uv

COPY pyproject.toml uv.lock ./
RUN uv pip install --system --no-cache

COPY . .

CMD ["uv", "run", "uvicorn", "terrarisk.main:app", "--host", "0.0.0.0", "--port", "8000"]
