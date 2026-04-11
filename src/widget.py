# делаем вызов функций из предыдущего модуля masks
# вызываю стандартную библиотеку для работы с датой
from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(input_string: str) -> str:
    """Обрабатываем строку о счете или карте и маскируем её"""
    separate = input_string.strip().split()
    if not separate:
        return "Введена пустая строка"
    number = separate[-1]
    sys_pay = " ".join(separate[:-1])
    if len(number) == 16 and number.isdigit():
        mask_number = get_mask_card_number(number)

    else:
        mask_number = get_mask_account(number)
    return f"{sys_pay}, {mask_number}"


def get_date(input_date: str) -> str:
    """Возфращаем формат даты согласно заданию"""
    try:
        dt_in = datetime.fromisoformat(input_date)
        # Форматируем в нужный вид
        format_date = dt_in.strftime("%d.%m.%Y")
        return format_date
    except ValueError as e:
        raise ValueError(
            f'Некорректный формат даты: {input_date}. Ожидаемый формат: "ГГГГ-ММ-ДДТЧЧ:ММ:СС.мммммм"'
        ) from e
