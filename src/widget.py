#делаем вызов функций из предыдущего модуля masks
#вызываю стандартную библиотеку для работы с датой
from .masks import get_mask_card_number, get_mask_account
from datetime import datetime

def mask_account_card(input_string: str) -> str:
    '''Обрабатываем строку о счете или карте и маскируем её'''
    separate = input_string.strip().split()
    if not separate:
        return 'Введена пустая строка'
    number = separate[-1]
    sys_pay = ' '.join(separate[:-1])
    if len(number) == 16 and number.isdigit():
        mask_number = get_mask_card_number(number)

    else:
        mask_number = get_mask_account(number)
    return f'}{sys_pay}, {mask_number}'



    pass

def get_date(date_string: str) -> str:
    '''Возфращаем формат даты согласно заданию'''
    pass