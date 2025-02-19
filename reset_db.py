from app import create_app, db
import os
import glob

def reset_database():
    # Xóa tất cả các file liên quan đến database
    files_to_remove = [
        'app.db',
        'migrations',
        '__pycache__',
        '*.pyc'
    ]

    for pattern in files_to_remove:
        for file_path in glob.glob(pattern, recursive=True):
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Đã xóa file: {file_path}")
            elif os.path.isdir(file_path):
                for root, dirs, files in os.walk(file_path, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(file_path)
                print(f"Đã xóa thư mục: {file_path}")

    app = create_app()
    with app.app_context():
        # Drop tất cả các bảng nếu tồn tại
        db.drop_all()
        print("Đã xóa tất cả các bảng cũ")
        
        # Tạo lại tất cả các bảng
        db.create_all()
        print("Đã tạo database mới với schema mới")

if __name__ == '__main__':
    reset_database()