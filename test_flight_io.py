from flight_io import read_flights_from_csv
from errors import InvalidKeyInFlightsFile
from io import StringIO
import pytest


def test_read_flights_from_csv():
    with open('flights_database.csv', 'r') as file_handle:
        flights = read_flights_from_csv(file_handle)
    assert flights[1].plane_number() == 1
    assert flights[2].plane_number() == 2
    assert flights[3].plane_number() == 3
    assert flights[4].plane_number() == 4
    assert flights[5].plane_number() == 5
    assert flights[6].plane_number() == 6
    assert flights[7].plane_number() == 7
    assert flights[8].plane_number() == 8
    assert flights[9].plane_number() == 9
    assert flights[10].plane_number() == 10


def test_read_flights_from_csv_negative_plane_number():
    data = 'plane_number\n1\n-1\n2\n'
    file_handle = StringIO(data)
    flights = read_flights_from_csv(file_handle)
    assert len(flights) == 2


def test_read_flights_from_csv_plane_number_float():
    data = 'plane_number\n1\n1.0\n34\n'
    file_handle = StringIO(data)
    flights = read_flights_from_csv(file_handle)
    assert len(flights) == 2


def test_read_flights_from_csv_doubled_new_line():
    data = 'plane_number\n2\n\n1\n'
    file_handle = StringIO(data)
    result = read_flights_from_csv(file_handle)
    assert len(result) == 2


def test_read_flights_from_csv_invalid_header():
    data = 'plane_num\n2\n\n1\n'
    file_handle = StringIO(data)
    with pytest.raises(InvalidKeyInFlightsFile):
        read_flights_from_csv(file_handle)


def test_read_passengers_from_csv_invalid_row():
    data = 'plane_num\na2\n\n1\n'
    file_handle = StringIO(data)
    with pytest.raises(InvalidKeyInFlightsFile):
        read_flights_from_csv(file_handle)
