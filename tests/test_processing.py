# Вызов фреймворка pytest и функций из processing

import pytest
from src.processing import filter_by_state, sort_by_date

@pytest.fixture
def sample_data():
    return [
        {'id': 414288290, 'state': 'EXECUTED', 'date': '2026-07-03T18:35:29.512364'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2024-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2022-06-30T02:08:58.425572'}
    ]

def test_filter_by_state(sample_data):
    result = filter_by_state(sample_data)
    assert len(result) == 2
    assert all(item["state"] == "EXECUTED" for item in result)

def test_sort_by_date_ascending(sample_data):
    result = sort_by_date(sample_data, reverse=False)
    dates = [item["date"] for item in result]
    expected_dates = [
        '2022-06-30T02:08:58.425572',
        '2024-09-12T21:27:25.241689',
        '2026-07-03T18:35:29.512364'
    ]
    assert dates == expected_dates

def test_sort_by_date_descending(sample_data):
    result = sort_by_date(sample_data, reverse=True)
    dates = [item["date"] for item in result]
    expected_dates = [
        '2026-07-03T18:35:29.512364',
        '2024-09-12T21:27:25.241689',
        '2022-06-30T02:08:58.425572'
    ]
    assert dates == expected_dates