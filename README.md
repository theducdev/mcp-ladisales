﻿# MCP LaDiSales Integration 🚀

## Giới thiệu

MCP LaDiSales là giải pháp tích hợp API của nền tảng LaDiSales, cho phép kết nối và đồng bộ dữ liệu theo thời gian thực (streamable-http) với các hệ thống khác. 

### 🛠 Tính năng chính

- **Quản lý sản phẩm**: 
  - Tạo mới, cập nhật, xóa sản phẩm
  - Quản lý biến thể và thuộc tính
  - Tìm kiếm và lọc sản phẩm

- **Quản lý khách hàng**:
  - Theo dõi thông tin khách hàng
  - Quản lý địa chỉ
  - Tags và trường tùy chỉnh

- **Quản lý khuyến mãi**:
  - Tạo chương trình giảm giá
  - Quản lý mã khuyến mãi
  - Cấu hình điều kiện áp dụng

- **Quản lý địa điểm**:
  - Dữ liệu địa giới hành chính
  - Hỗ trợ từ quốc gia đến phường/xã

### 💡 Lợi ích

Dự án này đặc biệt hữu ích cho các đơn vị cần tích hợp LaDiSales vào hệ thống của họ, mang lại:
- Tự động hóa quy trình
- Đồng bộ dữ liệu theo thời gian thực
- Tối ưu hóa trải nghiệm quản lý bán hàng đa kênh

## Hướng dẫn triển khai

### I. Triển khai MCP Server

#### Yêu cầu VPS:

- Python 3.13+
- Docker

#### Các bước cài đặt:

1. **Truy cập server qua SSH**

2. **Clone project về VPS:**
```bash
git clone https://github.com/theducdev/mcp-ladisales
cd mcp-ladisales
```

3. **Build và chạy container:**
```bash
sudo docker-compose up -d --build
```

> 💡 Khi hoàn tất, mcp server sẽ chạy ở http://<IP_VPS>:8000/mcp/

### II. Triển khai MCP Client bằng n8n

1. Tải source json n8n tại: [Download](https://drive.google.com/file/d/1Zz9_7iA8ceNHCX3VBou14SSc9bxFkKTV/view?usp=sharing)

2. Thay nội dung ở Endpoint của node MCP Client1 bằng url server vừa chạy thành công ở trên (dạng http://<IP_VPS>:8000/mcp)

## Tài liệu tham khảo

- [Model Context Protocol Python SDK](https://github.com/modelcontextprotocol/python-sdk) - Thư viện SDK chính thức cho việc phát triển MCP server và client
- [MCP Documentation](https://modelcontextprotocol.io) - Tài liệu chi tiết về Model Context Protocol
