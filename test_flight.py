from flight import Flight
from errors import InvalidPlaneNumber
import pytest


def test_flight_init_valid():
    fl = Flight(123)
    assert fl.plane_number() == 123


def test_flight_plane_number_is_zero():
    with pytest.raises(InvalidPlaneNumber):
        Flight(0)


def test_flight_plane_number_is_negative():
    with pytest.raises(InvalidPlaneNumber):
        Flight(-120)


def test_flight_str():
    fl = Flight(456)
    assert str(fl) == 'Flight: plane number: 456'
