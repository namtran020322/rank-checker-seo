# Hướng dẫn Triển khai Ứng dụng

## Triển khai trên PythonAnywhere

1. Đăng ký tài khoản tại [PythonAnywhere](https://www.pythonanywhere.com/)

2. Sau khi đăng nhập, tạo một Web app mới:
   - Chọn "Web" từ dashboard
   - Click "Add a new web app"
   - Chọn "Manual configuration"
   - Chọn Python version (3.8 hoặc cao hơn)

3. Thiết lập môi trường ảo:
```bash
mkvirtualenv --python=/usr/bin/python3.8 rank-checker-venv
```

4. Clone repository:
```bash
git clone https://github.com/yourusername/rank-checker.git
cd rank-checker
```

5. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

6. Cấu hình WSGI file (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):
```python
import sys
import os
from dotenv import load_dotenv

# Thêm đường dẫn đến thư mục dự án
path = '/home/yourusername/rank-checker'
if path not in sys.path:
    sys.path.append(path)

# Load biến môi trường
project_folder = os.path.expanduser(path)
load_dotenv(os.path.join(project_folder, '.env'))

# Import ứng dụng Flask
from run import app as application
```

7. Cấu hình các biến môi trường:
   - Trong PythonAnywhere dashboard, vào tab "Web"
   - Trong phần "Environment variables", thêm các biến sau:
     ```
     FLASK_APP=run.py
     FLASK_ENV=production
     SECRET_KEY=your-secret-key
     SERPER_API_KEY=your-serper-api-key
     ```

8. Reload web app trong PythonAnywhere dashboard

## Triển khai trên Heroku

1. Cài đặt [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

2. Đăng nhập Heroku:
```bash
heroku login
```

3. Tạo file `Procfile`:
```
web: gunicorn run:app
```

4. Tạo ứng dụng Heroku:
```bash
heroku create your-app-name
```

5. Thiết lập các biến môi trường:
```bash
heroku config:set FLASK_APP=run.py
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
heroku config:set SERPER_API_KEY=your-serper-api-key
```

6. Deploy ứng dụng:
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

7. Tạo database:
```bash
heroku run python reset_db.py
```

## Cài đặt SSL/HTTPS

### Trên PythonAnywhere
- SSL/HTTPS được cung cấp miễn phí cho các tên miền *.pythonanywhere.com
- Cho tên miền tùy chỉnh, bạn cần tài khoản trả phí

### Trên Heroku
- SSL/HTTPS được cung cấp tự động cho tất cả các ứng dụng

## Bảo mật

1. Đảm bảo các biến môi trường được cấu hình đúng cách
2. Sử dụng SECRET_KEY mạnh và ngẫu nhiên
3. Kích hoạt HTTPS
4. Cập nhật các dependencies thường xuyên
5. Thiết lập giám sát và cảnh báo
6. Backup database định kỳ

## Khắc phục sự cố

### Lỗi thường gặp

1. Application Error (H10) trên Heroku:
   - Kiểm tra logs: `heroku logs --tail`
   - Đảm bảo Procfile được cấu hình đúng
   - Kiểm tra requirements.txt

2. Database Connection Error:
   - Kiểm tra URL kết nối database
   - Đảm bảo database đã được khởi tạo

3. Internal Server Error (500):
   - Kiểm tra application logs
   - Xác nhận các biến môi trường đã được cấu hình
   - Kiểm tra quyền truy cập file

### Liên hệ Hỗ trợ

Nếu bạn gặp vấn đề không thể tự giải quyết, vui lòng:
1. Tạo issue trên GitHub repository
2. Gửi email đến địa chỉ hỗ trợ
3. Tham khảo documentation của nền tảng hosting