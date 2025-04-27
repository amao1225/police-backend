import os
from dotenv import load_dotenv

load_dotenv()  # 加载环境变量

class Config:
    # 基础配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:Yx123456789.@localhost/police_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION = 7200  # 2小时
    
    # 文件上传
    UPLOAD_FOLDER = './uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'pdf'}
    
    # 日志配置
    LOG_FILE = 'app.log'
    LOG_LEVEL = 'INFO'

    # 微信小程序配置
    WX_APPID = os.getenv('WX_APPID', 'your_appid')
    WX_SECRET = os.getenv('WX_SECRET', 'your_secret')