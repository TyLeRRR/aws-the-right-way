import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'not-today'
    STOCK_SYMBOL_SERVICE_URL = "http://localhost:5000/api/stocks"
    LOGO_RESIZER_SERVICE_URL = "http://localhost:5001/api/upload_image"
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
