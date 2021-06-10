from plane import Plane
from errors import (
    InvalidNumberOfSeats,
    InvalidCarrierName,
    InvalidPlaneNumber
)
import pytest


def test_init_plane_valid():
    plane = Plane(1223, 245, 50, 'Lot')
    assert plane.plane_number() == 1223
    assert plane.economic_seats_number() == 245
    assert plane.business_seats_number() == 50
    assert plane.carrier() == 'LOT'
    for seat in plane.economic_seats_occupancy():
        assert plane.economic_seats_occupancy()[seat] == 'FREE'
    for seat in plane.business_seats_occupancy():
        assert plane.business_seats_occupancy()[seat] == 'FREE'
    assert len(plane.busy_assistnats()) == 0


def test_init_plane_number_zero():
    with pytest.raises(InvalidPlaneNumber):
        Plane(0, 123, 5, 'lot')


def test_init_plane_number_negative():
    with pytest.raises(InvalidPlaneNumber):
        Plane(-10, 123, 10, 'lot')


def test_init_plane_number_not_int():
    with pytest.raises(InvalidPlaneNumber):
        Plane(10.5, 123, 10, 'lot')


def test_init_plane_economic_seat_number_zero():
    with pytest.raises(InvalidNumberOfSeats):
        Plane(10, 0, 50, 'lot')


def test_init_plane_economic_seat_number_negative():
    with pytest.raises(InvalidNumberOfSeats):
        Plane(10, -123, 10, 'lot')


def test_init_plane_economic_seat_number_not_int():
    with pytest.raises(InvalidNumberOfSeats):
        Plane(105, 1.23, 2, 'lot')


def test_init_plane_business_seat_number_zero():
    with pytest.raises(InvalidNumberOfSeats):
        Plane(10, 10, 0, 'LOT')


def test_init_plane_business_seat_number_negative():
    with pytest.raises(InvalidNumberOfSeats):
        Plane(10, 1, -123, 'LOT')


def test_init_plane_business_seat_number_not_int():
    with pytest.raises(InvalidNumberOfSeats):
        Plane(105, 2, 1.23, 'LOT')


def test_plane_carrier_lower_case():
    plane = Plane(1223, 245, 50, 'lot')
    assert plane.carrier() == 'LOT'


def test_plane_carrier_upper_case():
    plane = Plane(1223, 245, 50, 'AMERICA AIRLINES')
    assert plane.carrier() == 'AMERICA AIRLINES'


def test_plane_carrier_mixed_case_letters():
    plane = Plane(1223, 245, 50, 'AmErica aIRLINES')
    assert plane.carrier() == 'AMERICA AIRLINES'


def test_plane_carrier_empty():
    with pytest.raises(InvalidCarrierName):
        Plane(1223, 245, 50, '')


def test_plane_str():
    plane = Plane(45, 20, 10, 'LOT')
    description = 'Plane: plane number: 45, economic seats number: 20'
    description += ', business seats number: 10, carrier: LOT'
    str_plane = str(plane)
    assert str_plane == description
