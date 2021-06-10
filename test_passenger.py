from passenger import Passenger
from errors import (
    InvalidPassengerFirstName,
    InvalidPassengerLastName,
    InvalidPassengerTicketID
)
import pytest


def test_init_valid():
    person = Passenger('FName', 'LName', '012345')
    assert person.first_name() == 'FName'
    assert person.last_name() == 'LName'
    assert person.ticket_id() == '012345'


def test_init_invalid_first_name_empty():
    with pytest.raises(InvalidPassengerFirstName):
        Passenger('', 'LName', '012345')


def test_init_invalid_first_name_list():
    with pytest.raises(InvalidPassengerFirstName):
        Passenger([], 'LName', '012345')


def test_init_invalid_last_name_empty():
    with pytest.raises(InvalidPassengerLastName):
        Passenger('FName', '', '012345')


def test_init_invalid_last_name_list():
    with pytest.raises(InvalidPassengerLastName):
        Passenger('FName', [], '012345')


def test_init_invalid_ticket_id_empty():
    with pytest.raises(InvalidPassengerTicketID):
        Passenger('FName', 'LName', '')


def test_init_invalid_ticket_id_list():
    with pytest.raises(InvalidPassengerTicketID):
        Passenger('FName', 'LName', [])


def test_passenger_str():
    person = Passenger('John', 'McClayne', 49)
    description = 'Passenger: John McClayne, ticket id number: 49'
    assert str(person) == description
