# Вызываю стандартную функцию для конвертирования даты согласно заданию

from datetime import datetime

def filter_by_state(filt_d: list[dict], state: str ='EXECUTED') -> list[dict]:
    """Фильтрует список словарей по state"""
    for f in filt_d:
        if f.get('state') == state:
        return f


def sort_by_date(filt_d: list[dict], reverse: bool = True) -> list[dict]:
    '''Функция сортировки по дате'''
    def sort_date(date_s: str) -> datetime:
        try:
            return datetime.strptime(date_s, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            return datetime.min

        return sorted(filt_d, key=lambda x: sort_date(x.get('date', '')), reverse=reverse)
