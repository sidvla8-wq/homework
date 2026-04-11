#делаем вызов функций из предыдущего модуля masks
#вызываю стандартную библиотеку для работы с датой
from .masks import get_mask_card_number, get_mask_account
from datetime import datetime

def mask_account_card(input_string: str) -> str:
    '''Обрабатываем строку о счете или карте и маскируем её'''
    pass

def get_date(date_string: str) -> str:
    ''' '''
    pass