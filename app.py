from flask import Flask
from config import Config  # 直接导入根目录的config
from extensions import db, migrate, cors
import logging
from logging.handlers import RotatingFileHandler

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)  # 确保migrate正确关联db
    cors.init_app(app)
    
    # 注册蓝图（确保蓝图路径正确）
    from blueprints.auth import auth_bp
    from blueprints.case import case_bp
    from blueprints.task import task_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(case_bp)
    app.register_blueprint(task_bp)
    
    # 日志配置（不变）
    file_handler = RotatingFileHandler(
        app.config['LOG_FILE'], 
        maxBytes=10240, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)