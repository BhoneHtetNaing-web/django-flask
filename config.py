class Config:
    SECRET_KEY = "super-secret-key"
    SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}