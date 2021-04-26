import os

currentdir = os.path.abspath(os.path.dirname(__file__))


class Configuration:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(currentdir, 'app/app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
    STORAGE='images'  # название папки с изображениями, всегда находится в app/static
    NAME = 'blog'
    POSTS_BY_PAGE = 5
    SEARCH = ['title', 'text']  # настройки поиска. title - по заголовкам, text - по тексту
