import os
from tai_alphi import Alphi

settings = {
    'logger1': {
        'consola': {
            'enabled': True,
            'log_level': 'DEBUG',
            'display_info': ['asctime', 'levelname', 'module', 'lineno'],
            'time_format': '%Y-%m-%d %H:%M:%S'
        },
        'teams': {
            'enabled': False,
            'log_level': 'INFO',
            'display_info': ['asctime', 'levelname'],
            'time_format': '%Y-%m-%d %H:%M:%S',
            'project': 'DigitHens',
            'pipeline': 'csv_data_loader',
            'notifications': ['crama@triplealpha.in']
        }
    }
}

bot = Alphi(settings)

logger = bot.get_logger(logger_name='logger1')