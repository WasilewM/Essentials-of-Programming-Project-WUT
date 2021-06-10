from plane_io import read_planes_from_csv
from errors import InvalidKeyInPlanesFile
from io import StringIO
import pytest


def test_read_planes_from_csv():
    with open('planes_database.csv', 'r') as file_handle:
        planes = read_planes_from_csv(file_handle)

    assert planes[1].plane_number() == 1
    assert planes[2].plane_number() == 2
    assert planes[3].plane_number() == 3
    assert planes[4].plane_number() == 4
    assert planes[5].plane_number() == 5
    assert planes[6].plane_number() == 6
    assert planes[7].plane_number() == 7
    assert planes[8].plane_number() == 8
    assert planes[9].plane_number() == 9
    assert planes[10].plane_number() == 10


def test_read_planes_from_csv_negative_plane_number():
    data = 'plane_number,economic_seats_number,business_seats_number,carrier\n'
    data += '-1,1,1,LOT\n1,1,1,LOT\n2,2,2,LOT\n'
    file_handle = StringIO(data)
    planes = read_planes_from_csv(file_handle)
    assert len(planes) == 2


def test_read_planes_from_csv_plane_number_float():
    data = 'plane_number,economic_seats_number,business_seats_number,carrier\n'
    data += '1.0,1,1,LOT\n1,1,1,LOT\n2,2,2,LOT\n'
    file_handle = StringIO(data)
    planes = read_planes_from_csv(file_handle)
    assert len(planes) == 2


def test_read_planes_from_csv_economic_seats_number_float():
    data = 'plane_number,economic_seats_number,business_seats_number,carrier\n'
    data += '1,1.0,1,LOT\n1,1,1,LOT\n2,2,2,LOT\n'
    file_handle = StringIO(data)
    planes = read_planes_from_csv(file_handle)
    assert len(planes) == 2


def test_read_planes_from_csv_negative_economic_seats():
    data = 'plane_number,economic_seats_number,business_seats_number,carrier\n'
    data += '1,-10,10,LOT\n1,1,1,LOT\n2,2,2,LOT\n3,10,20,AMEricaAirlines\n'
    file_handle = StringIO(data)
    planes = read_planes_from_csv(file_handle)
    assert len(planes) == 3


def test_read_planes_from_csv_economic_seats_is_zero():
    data = 'plane_number,economic_seats_number,business_seats_number,carrier\n'
    data += '1,0,20,LOT\n40,50,40,UKLines\n'
    file_handle = StringIO(data)
    planes = read_planes_from_csv(file_handle)
    assert len(planes) == 1


def test_read_planes_from_csv_business_seats_number_float():
    data = 'plane_number,economic_seats_number,business_seats_number,carrier\n'
    data += '1,1,1.0,LOT\n50,60,78,LOT\n'
    file_handle = StringIO(data)
    planes = read_planes_from_csv(file_handle)
    assert len(planes) == 1


def test_read_planes_from_csv_negative_business_seats():
    data = 'plane_number,economic_seats_number,business_seats_number,carrier\n'
    data += '1,1,-10,LOT\n1,2,4,LOT\n2,10,50,LOT\n'
    file_handle = StringIO(data)
    planes = read_planes_from_csv(file_handle)
    assert len(planes) == 2


def test_read_planes_from_csv_business_seats_is_zero():
    data = 'plane_number,economic_seats_number,business_seats_number,carrier\n'
    data += '1,1,0,LOT\n1,2,4,LOT\n2,10,50,LOT\n100,100,100,LOT\n3,3,3,LOT\n'
    file_handle = StringIO(data)
    planes = read_planes_from_csv(file_handle)
    assert len(planes) == 4


def test_read_planes_from_csv_missing_column():
    data = 'plane_number,economic_seats_numberbusiness_seats_number,carrier\n'
    data += '1,1,1,LOT\n'
    file_handle = StringIO(data)
    with pytest.raises(InvalidKeyInPlanesFile):
        read_planes_from_csv(file_handle)


def test_read_planes_from_csv_invalid_carrier():
    data = 'plane_number,economic_seats_numberbusiness_seats_number,carrier\n'
    data += '1,1,1,[]\n'
    file_handle = StringIO(data)
    with pytest.raises(InvalidKeyInPlanesFile):
        read_planes_from_csv(file_handle)
