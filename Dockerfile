FROM python:3.13-rc-slim

WORKDIR /app

# Cài đặt các dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && \
    uv pip install -e .

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"] 