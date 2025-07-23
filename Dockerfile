FROM python:3.13-rc-slim

WORKDIR /app

# Cài đặt các dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Run the application using uv
CMD ["uv", "run", "main.py"] 