#делаем вызов функций из предыдущего модуля
from .masks import get_mask_card_number, get_mask_account


def mask_account_card(input_string: str) -> str:
    '''Обрабатываем строку о счете или карте и маскируем её'''
    pass