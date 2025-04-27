# /home/ubuntu/bash/alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import sys
from os.path import abspath, dirname

# 添加项目根目录到Python路径
sys.path.insert(0, dirname(dirname(abspath(__file__))))

# 强制导入所有模型（关键修复）
from app.models.user import User
from app.models.case import Case
from app.models.task import Task
from app.extensions import db

config = context.config
fileConfig(config.config_file_name)
target_metadata = db.Model.metadata  # 绑定统一元数据

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_suffix),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True
        )
        with context.begin_transaction():
            context.run_migrations()