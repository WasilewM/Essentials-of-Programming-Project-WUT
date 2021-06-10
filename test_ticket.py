from ticket import Ticket
from errors import (
    InvalidTicketIDNumber,
    InvalidGateNumber,
    InvalidSeatNumber,
    InvalidSeatClass,
    InvalidPlaneNumber
)
import pytest


def test_init_ticket_valid():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    assert ticket.ticket_id() == '012345'
    assert ticket.plane_number() == 123
    assert ticket.seat_class() == 'business'
    assert ticket.seat_number() == 16
    assert ticket.gate_number() == 7


def test_init_ticket_number_empty():
    with pytest.raises(InvalidTicketIDNumber):
        Ticket('', 123, 'business', 16, 7)


def test_init_plane_number_is_zero():
    with pytest.raises(InvalidPlaneNumber):
        Ticket('012345', 0, 'business', 16, 7)


def test_init_plane_number_is_negative():
    with pytest.raises(InvalidPlaneNumber):
        Ticket('012345', -100, 'business', 16, 7)


def test_init_plane_number_not_int():
    with pytest.raises(InvalidPlaneNumber):
        Ticket('012345', 0.1, 'business', 16, 7)


def test_init_seat_number_is_zero():
    with pytest.raises(InvalidSeatNumber):
        Ticket('012345', 10, 'business', 0, 7)


def test_init_seat_number_is_negative():
    with pytest.raises(InvalidSeatNumber):
        Ticket('012345', 100, 'business', -16, 7)


def test_init_seat_number_not_int():
    with pytest.raises(InvalidSeatNumber):
        Ticket('012345', 123, 'business', 16.4, 7)


def test_init_gate_number_is_zero():
    with pytest.raises(InvalidGateNumber):
        Ticket('012345', 10, 'business', 10, 0)


def test_init_gate_number_is_negative():
    with pytest.raises(InvalidGateNumber):
        Ticket('012345', 100, 'business', 16, -7)


def test_init_gate_number_not_int():
    with pytest.raises(InvalidGateNumber):
        Ticket('012345', 123, 'business', 16, 7.09)


def test_ticket_set_seat_number_valid():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    assert ticket.seat_number() == 16
    ticket.set_seat_number(5)
    assert ticket.seat_number() == 5


def test_ticket_set_seat_number_zero():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    assert ticket.seat_number() == 16
    with pytest.raises(InvalidSeatNumber):
        ticket.set_seat_number(0)


def test_ticket_set_seat_number_negative():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    assert ticket.seat_number() == 16
    with pytest.raises(InvalidSeatNumber):
        ticket.set_seat_number(-51)


def test_ticket_set_seat_number_not_int():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    assert ticket.seat_number() == 16
    with pytest.raises(InvalidSeatNumber):
        ticket.set_seat_number(5.3)


def test_ticket_seat_class_business():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    assert ticket.seat_class() == 'business'


def test_ticket_seat_class_economic():
    ticket = Ticket('012345', 123, 'economic', 16, 7)
    assert ticket.seat_class() == 'economic'


def test_ticekt_seat_class_invalid():
    with pytest.raises(InvalidSeatClass):
        Ticket('012345', 123, 'first', 16, 7)


def test_ticket_seat_class_empty():
    with pytest.raises(InvalidSeatClass):
        Ticket('012345', 123, 'ecomonic', 16, 7)


def test_ticekt_seat_class_invalid_random_str():
    with pytest.raises(InvalidSeatClass):
        Ticket('012345', 123, 'sfgg', 16, 7)


def test_ticket_str():
    ticket = Ticket('023', 12, 'business', 4, 3)
    description = 'Ticket: id: 023, plane number: 12, '
    description += 'seat class: business, seat number: 4, '
    description += 'gate number: 3'
    assert str(ticket) == description


def test_init_ticket_sest_number_valid():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    ticket.set_seat_number(124)
    assert ticket.seat_number() == 124


def test_init_ticket_sest_number_negative():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    with pytest.raises(InvalidSeatNumber):
        ticket.set_seat_number(-124)


def test_init_ticket_sest_number_str():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    with pytest.raises(InvalidSeatNumber):
        ticket.set_seat_number('124')


def test_init_ticket_sest_class_valid():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    ticket.set_seat_class('economic')
    assert ticket.seat_class() == 'economic'


def test_init_ticket_sest_class_for_the_same_class():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    ticket.set_seat_class('business')
    assert ticket.seat_class() == 'business'


def test_init_ticket_sest_class_invalid():
    ticket = Ticket('012345', 123, 'business', 16, 7)
    with pytest.raises(InvalidSeatClass):
        ticket.set_seat_class('asfsg')
