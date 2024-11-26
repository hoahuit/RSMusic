from app import create_app

# Tạo ứng dụng Flask
app = create_app()

if __name__ == '__main__':
    # Khởi chạy Flask server
    app.run(debug=True)
