# Вызываю стандартную функцию для конвертирования даты согласно заданию

from datetime import datetime

def filter_by_state(filt_operation: list[dict], state: str ='EXECUTED') -> list[dict]:
    """Фильтрует список словарей по state"""
    return [f for f in filt_operation if f.get('state') == state]


def sort_by_date(filt_operation: list[dict], reverse: bool = True) -> list[dict]:
    '''Функция сортировки по дате'''
    def sort_date(date_s: str) -> datetime:
        try:
            return datetime.strptime(date_s, '%Y-%m-%d').date()
        except ValueError:
            return datetime.min

    return sorted(
        filt_operation,
        key=lambda x: sort_date(x.get('date', '')),
        reverse=reverse
    )
