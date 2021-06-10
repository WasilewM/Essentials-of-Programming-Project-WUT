from passenger_io import read_passengers_from_csv
from errors import InvalidKeyInPassengersFile
import pytest
from io import StringIO


def test_read_passengers_from_csv():
    with open('passengers_database.csv', 'r') as file_handle:
        passengers = read_passengers_from_csv(file_handle)
    assert passengers['1'].first_name() == 'Lara'
    assert passengers['1'].last_name() == 'Croft'
    assert passengers['1'].ticket_id() == '1'


def test_read_passengers_from_csv_invalid_headline():
    data = 'first_namelast_name,ticket_id\n'
    data += 'Jan,Kowalski,9'
    file_handle = StringIO(data)
    with pytest.raises(InvalidKeyInPassengersFile):
        read_passengers_from_csv(file_handle)


def test_read_passengers_from_csv_omit_invalid_data_line():
    data = 'first_name,last_name,ticket_id\n'
    data += 'Jan,Kowalski,1\n'
    data += 'AdamSiadam,2\n'
    data += 'Adam,Siadam,2'
    file_handle = StringIO(data)
    passengers = read_passengers_from_csv(file_handle)
    assert len(passengers) == 2
