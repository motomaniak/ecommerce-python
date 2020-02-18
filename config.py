class Config(object):
    DEBUG=False
    TESTING=False
    SECRET_KEY='2X6An*@K2x@GHkck'
    JWT_SECRET_KEY='rW27%NkfVQMUq%hnj%9RCp&9s$pkpfqVNwbbuwn'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI='postgresql+psycopg2://aaron:rR65!QPWBN%K@localhost:5432/ecommerce'

class DevelopmentConfig(Config):
    DEBUG=True
    FLASK_ENV='development'

class ProductionConfig(Config):
    FLASK_ENV='production'

config_settings = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}