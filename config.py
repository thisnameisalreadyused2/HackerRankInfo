class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    SECRET_KEY = b'NS\xcb\xd78\x97_r\x1c\xf8\xf1\x95\x9dp\xfc\x93F2\xd0\x83i\x92\xad\x9c\xc4BA\xce5R|\x95\xa1\xd3\xe0\x0f5\xe0\n\x92\xdad\xc1\x14\x9b>\xa41()\xd5\x7fm\xd4\x80W\x1ef\xb5\xcc\xa3\x91y\xcb'