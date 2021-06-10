from ticket_io import read_tickets_from_csv
from errors import InvalidKeyInTicketsFile
from io import StringIO
import pytest


def test_read_tickets_from_csv():
    with open('tickets_database.csv', 'r') as file_handle:
        tickets = read_tickets_from_csv(file_handle)

    assert tickets['1'].ticket_id() == '1'
    assert tickets['1'].plane_number() == 1
    assert tickets['1'].seat_class() == 'business'
    assert tickets['1'].seat_number() == 1
    assert tickets['1'].gate_number() == 1
    assert len(tickets) == 10


def test_read_planes_from_csv_invalid_headline():
    data = 'ticket_id,plane_number,seat_classseat_number,gate_number\n'
    data += '1,1,business,1,1\n'
    file_handle = StringIO(data)
    with pytest.raises(InvalidKeyInTicketsFile):
        read_tickets_from_csv(file_handle)


def test_read_planes_from_csv_negative_plane_number():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,-21,business,1,1\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0


def test_read_planes_from_csv_plane_number_is_zero():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,0,business,1,1\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0


def test_read_planes_from_csv_plane_number_is_float():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,2.0,business,1,1\n1,1,economic,1,1\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 1


def test_read_planes_from_csv_plane_number_is_str():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,bl,business,1,1\n1,1,economic,1,1\n2,1,business,2,2\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 2


def test_read_tickets_from_csv_seat_class_literal():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,busines,4,1\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0


def test_read_tickets_from_csv_seat_class_invalid():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,fdgisbf,4,1\n1,1,economic,1,1\n2,1,business,2,2\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 2


def test_read_planes_from_csv_negative_seat_number():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,business,-3,1\n'
    file_handle = StringIO(data)
    tikcets = read_tickets_from_csv(file_handle)
    assert len(tikcets) == 0


def test_read_planes_from_csv_seat_number_is_float():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,business,7.3,1\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0


def test_read_planes_from_csv_seat_number_is_str():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,business,aty,1\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0


def test_read_tickets_from_csv_negative_gate_number():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,business,4,-1\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0


def test_read_tickets_from_csv_gate_number_is_zero():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,business,4,0\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0


def test_read_tickets_from_csv_gate_number_is_float():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,business,4,5.0\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0


def test_read_tickets_from_csv_gate_number_is_str():
    data = 'ticket_id,plane_number,seat_class,seat_number,gate_number\n'
    data += '1,1,business,4,a0\n'
    file_handle = StringIO(data)
    tickets = read_tickets_from_csv(file_handle)
    assert len(tickets) == 0
