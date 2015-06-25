__title__ = 'pytgbotapi'
__version__ = '0.1'
__author__ = 'Yusuf Kaka'
__license__ = 'GPL v2'
__copyright__ = 'Copyright 2015 Yusuf Kaka'


import logging


# No logging unless the client provides a handler
logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ['BotApi']

