# Rank Checker

Ứng dụng web kiểm tra thứ hạng từ khóa và trạng thái index của website trên Google Search.

## Tính năng

- Kiểm tra thứ hạng từ khóa trên Google Search
- Hỗ trợ kiểm tra nhiều từ khóa + URL cùng lúc
- Kiểm tra trạng thái index của URL trên Google
- Xuất kết quả dạng Excel hoặc CSV
- Hỗ trợ đa ngôn ngữ và đa thiết bị
- Phân trang kết quả

## Yêu cầu hệ thống

- Python 3.8+
- Flask 3.0.2
- SQLAlchemy
- Các package khác được liệt kê trong file requirements.txt

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/yourusername/rank-checker.git
cd rank-checker
```

2. Tạo và kích hoạt môi trường ảo:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Cài đặt các dependencies:
```bash
pip install -r requirements.txt
```

4. Tạo file .env và cấu hình các biến môi trường:
```
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
SERPER_API_KEY=your-serper-api-key
```

5. Khởi tạo database:
```bash
python reset_db.py
```

6. Chạy ứng dụng:
```bash
python run.py
```

## Triển khai

Ứng dụng này là một ứng dụng web động sử dụng Flask và cần được triển khai trên một web server hỗ trợ Python. Một số lựa chọn phù hợp:

- Heroku
- PythonAnywhere
- DigitalOcean
- AWS Elastic Beanstalk

**Lưu ý:** Ứng dụng này không phù hợp để triển khai trên GitHub Pages vì GitHub Pages chỉ hỗ trợ các trang web tĩnh.

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request nếu bạn muốn cải thiện ứng dụng.

## Giấy phép

[MIT License](LICENSE)