# /home/ubuntu/bash/setup.py
from setuptools import setup, find_packages

setup(
    name="bash",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-sqlalchemy',
        'flask-migrate',
    ],
)