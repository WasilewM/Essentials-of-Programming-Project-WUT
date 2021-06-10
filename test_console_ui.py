from console_ui import (
    load_data,
    create_table
)
from database import Database


def test_load_data():
    db = Database()
    load_data(db)
    assert len(db.flights()) == 10
    assert len(db.planes()) == 10
    assert len(db.tickets()) == 10
    assert len(db.passengers()) == 10


def test_create_table():
    data = {'key': '1'}
    table = create_table(data)
    correct = """------------
| key |  1 |
------------
"""
    assert correct == table


def test_boarding_pass():
    table_data = {
        'ticket id': '1',
        'first name': 'Lara',
        'last name': 'Croft',
        'plane number': 1,
        'seat class': 'business',
        'seat number': 1,
        'gate number': 1,
    }

    boarding_pass = create_table(table_data)

    correct = """------------------------------
| ticket id    |           1 |
------------------------------
| first name   |        Lara |
------------------------------
| last name    |       Croft |
------------------------------
| plane number |           1 |
------------------------------
| seat class   |    business |
------------------------------
| seat number  |           1 |
------------------------------
| gate number  |           1 |
------------------------------
"""

    assert boarding_pass == correct


def test_flight_params():
    data = {
        'flight number': 1,
        'plane type': 'wide-body',
        'number of business class seats': 50,
        'number of economy class seats': 200,
        'carrier name': 'LOT'
    }
    table = create_table(data)

    correct = """------------------------------------------------------------------
| flight number                  |                             1 |
------------------------------------------------------------------
| plane type                     |                     wide-body |
------------------------------------------------------------------
| number of business class seats |                            50 |
------------------------------------------------------------------
| number of economy class seats  |                           200 |
------------------------------------------------------------------
| carrier name                   |                           LOT |
------------------------------------------------------------------
"""

    assert table == correct


def test_departure_gate():
    data = {'departure gate': 1}
    table = create_table(data)

    correct = """----------------------------------
| departure gate |             1 |
----------------------------------
"""

    assert table == correct
