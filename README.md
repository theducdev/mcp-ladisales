# MCP LaDiSales Integration

API integration with streamable-http support for LaDiSales

## Yêu cầu

- Python 3.13+
- Docker (tùy chọn)

## Cài đặt và Chạy

### Sử dụng Docker

1. Build và chạy container:
```bash
docker-compose up --build
```

MCP Server sẽ chạy với streamable-http support.

### Cài đặt thông thường

1. Cài đặt dependencies:

```
pip install uv
```

```
uv sync
```

2. Chạy server:
```bash
uv run main.py
```
