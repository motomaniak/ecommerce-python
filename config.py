import os

class Config():
    DEBUG=True

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

config_settings = {
    'development': DevelopmentConfig
}