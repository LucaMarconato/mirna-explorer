import os
from enum import Enum

DIR = os.path.dirname(os.path.realpath(__file__))


class AssetsMapper(Enum):
    APP_ICON = f'{DIR}/img/icon.png'
