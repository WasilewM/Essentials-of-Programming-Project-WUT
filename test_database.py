from database import Database
from errors import (
    FilePathNotFoundError,
    FileIsADirectoryError,
    InvalidSeatNumber,
    InvalidFileHeaderError,
    AllAssistantsAreBusyError,
    ChosenPassengerHasNotAskedForHelp,
    ChosenSeatIsOccupied
)
from flight import Flight
from passenger import Passenger
from plane import Plane
from ticket import Ticket
import pytest


def test_database_init():
    db = Database()
    assert len(db.flights()) == 0
    assert len(db.passengers()) == 0
    assert len(db.planes()) == 0
    assert len(db.tickets()) == 0


def test_database_read_flights_valid():
    db = Database()
    db.read_flights('flights_database.csv')
    assert len(db.flights()) == 10
    assert db.flights()[1].plane_number() == 1
    assert db.flights()[10].plane_number() == 10


def test_database_read_flights_invalid_file_name():
    with pytest.raises(FilePathNotFoundError):
        db = Database()
        db.read_flights('flight_database.csv')


def test_database_read_flights_file_is_a_directory():
    with pytest.raises(FileIsADirectoryError):
        db = Database()
        db.read_flights('/')


def test_database_read_flights_invalid_header():
    with pytest.raises(InvalidFileHeaderError):
        db = Database()
        db.read_flights('invalid_header_test.csv')


def test_database_read_passengers_valid():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')
    assert len(db.passengers()) == 10

    assert db.passengers()['1'].ticket_id() == '1'
    assert db.passengers()['1'].first_name() == 'Lara'
    assert db.passengers()['1'].last_name() == 'Croft'

    assert db.passengers()['10'].ticket_id() == '10'
    assert db.passengers()['10'].first_name() == 'Stefan'
    assert db.passengers()['10'].last_name() == 'Zolkiewski'


def test_database_read_passengers_invalid_file_name():
    with pytest.raises(FilePathNotFoundError):
        db = Database()
        db.read_passengers('some_database.csv')


def test_database_read_passengers_file_is_a_directory():
    with pytest.raises(FileIsADirectoryError):
        db = Database()
        db.read_passengers('/')


def test_database_read_passenger_invalid_header():
    with pytest.raises(InvalidFileHeaderError):
        db = Database()
        db.read_passengers('invalid_header_test.csv')


def test_database_read_planes_valid():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')
    assert len(db.planes()) == 10

    assert db.planes()[1].plane_number() == 1
    assert db.planes()[1].economic_seats_number() == 200
    assert db.planes()[1].business_seats_number() == 50
    assert db.planes()[1].carrier() == 'LOT'

    assert db.planes()[7].plane_number() == 7
    assert db.planes()[7].economic_seats_number() == 224
    assert db.planes()[7].business_seats_number() == 26
    assert db.planes()[7].carrier() == 'WIZZAIR'


def test_database_read_planes_invalid_file_name():
    with pytest.raises(FilePathNotFoundError):
        db = Database()
        db.read_planes('some_database.csv')


def test_database_read_planes_file_is_a_directory():
    with pytest.raises(FileIsADirectoryError):
        db = Database()
        db.read_planes('/')


def test_database_read_planes_invalid_header():
    with pytest.raises(InvalidFileHeaderError):
        db = Database()
        db.read_planes('invalid_header_test.csv')


def test_database_read_tickets_valid():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')
    assert len(db.tickets()) == 10

    assert db.tickets()['3'].ticket_id() == '3'
    assert db.tickets()['3'].plane_number() == 1
    assert db.tickets()['3'].seat_class() == 'business'
    assert db.tickets()['3'].seat_number() == 20
    assert db.tickets()['3'].gate_number() == 1

    assert db.tickets()['7'].ticket_id() == '7'
    assert db.tickets()['7'].plane_number() == 1
    assert db.tickets()['7'].seat_class() == 'economic'
    assert db.tickets()['7'].seat_number() == 3
    assert db.tickets()['7'].gate_number() == 1


def test_database_read_tickets_invalid_file_name():
    with pytest.raises(FilePathNotFoundError):
        db = Database()
        db.read_tickets('some_database.csv')


def test_database_read_tickets_file_is_a_directory():
    with pytest.raises(FileIsADirectoryError):
        db = Database()
        db.read_tickets('/')


def test_database_read_tickets_invalid_header():
    with pytest.raises(InvalidFileHeaderError):
        db = Database()
        db.read_tickets('invalid_header_test.csv')


def test_database_add_flights_valid():
    db = Database()
    fl = Flight(4)
    db.add_flight(fl)
    assert len(db.flights()) == 1
    assert db.flights()[4] == fl


def test_database_add_flight_already_exists():
    db = Database()
    db.read_flights('flights_database.csv')
    fl = Flight(4)
    detected_existing_keys = db.add_flight(fl)
    assert detected_existing_keys == 1


def test_database_add_passenger_valid():
    db = Database()
    fl = Flight(1)
    db.add_flight(fl)
    plane = Plane(1, 300, 50, 'LOT')
    db.add_plane(plane)
    ticket = Ticket('123', 1, 'economic', 1, 1)
    db.add_ticket(ticket)
    person = Passenger('FName', 'LName', '123')
    db.add_passenger(person)
    assert len(db.passengers()) == 1
    assert db.passengers()['123'] == person


def test_database_add_passenger_already_exists():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')
    person = Passenger('FName', 'LName', '1')
    detected_existing_keys = db.add_passenger(person)
    assert detected_existing_keys == 1


def test_database_add_plane_valid():
    db = Database()
    fl = Flight(1)
    db.add_flight(fl)
    plane = Plane(1, 1, 1, 'LOT')
    db.add_plane(plane)
    assert len(db.planes()) == 1
    assert db.planes()[1] == plane


def test_database_add_plane_already_exists():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')
    plane = Plane(1, 1, 1, 'LOT')
    detected_existing_keys = db.add_plane(plane)
    assert detected_existing_keys == 1


def test_database_add_ticket_valid():
    db = Database()
    db.add_flight(Flight(1))
    plane = Plane(1, 300, 50, 'LOT')
    db.add_plane(plane)
    ticket = Ticket('4', 1, 'business', 1, 5)
    db.add_ticket(ticket)
    assert len(db.tickets()) == 1
    assert db.tickets()['4'] == ticket


def test_database_add_ticket_already_exists():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')
    ticket = Ticket('1', 1, 'economic', 1, 1)
    detected_existing_keys = db.add_ticket(ticket)
    assert detected_existing_keys == 1


def test_database_read_planes_seat_occupancy():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')

    for plane in db.planes():
        plane = db.planes()[plane]
        for seat in plane.economic_seats_occupancy():
            assert plane.economic_seats_occupancy()[seat] == 'FREE'
        for seat in plane.business_seats_occupancy():
            assert plane.business_seats_occupancy()[seat] == 'FREE'

    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')
    assert len(db.planes()) == 10

    assert db.planes()[1].plane_number() == 1
    assert db.planes()[1].economic_seats_number() == 200
    assert db.planes()[1].business_seats_number() == 50
    assert db.planes()[1].carrier() == 'LOT'

    assert db.planes()[7].plane_number() == 7
    assert db.planes()[7].economic_seats_number() == 224
    assert db.planes()[7].business_seats_number() == 26
    assert db.planes()[7].carrier() == 'WIZZAIR'

    assert db.planes()[1].economic_seats_occupancy()[1] == 'OCCUPIED'
    assert db.planes()[1].economic_seats_occupancy()[2] == 'OCCUPIED'
    assert db.planes()[1].economic_seats_occupancy()[3] == 'OCCUPIED'
    assert db.planes()[1].economic_seats_occupancy()[4] == 'OCCUPIED'
    assert db.planes()[1].economic_seats_occupancy()[5] == 'OCCUPIED'
    assert db.planes()[1].economic_seats_occupancy()[6] == 'OCCUPIED'
    assert db.planes()[1].economic_seats_occupancy()[10] == 'FREE'

    assert db.planes()[1].business_seats_occupancy()[1] == 'OCCUPIED'
    assert db.planes()[1].business_seats_occupancy()[10] == 'OCCUPIED'
    assert db.planes()[1].business_seats_occupancy()[20] == 'OCCUPIED'
    assert db.planes()[1].business_seats_occupancy()[30] == 'OCCUPIED'
    assert db.planes()[1].business_seats_occupancy()[35] == 'FREE'


def test_database_book_business_seat_valid():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    ticket = Ticket('1', 1, 'business', 1, 2)
    db.book_seat(ticket)
    assert db.planes()[1].business_seats_occupancy()[1] == 'OCCUPIED'


def test_database_book_economic_seat_valid():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    ticket = Ticket('1', 1, 'economic', 1, 2)
    db.book_seat(ticket)
    assert db.planes()[1].economic_seats_occupancy()[1] == 'OCCUPIED'


def test_database_book_business_seat_already_occupied():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    ticket = Ticket('1', 1, 'business', 1, 2)
    db.book_seat(ticket)
    ticket = Ticket('2', 1, 'business', 1, 2)

    with pytest.raises(ChosenSeatIsOccupied):
        db.book_seat(ticket)


def test_database_book_economic_seat_already_occupied():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    ticket = Ticket('1', 1, 'economic', 1, 2)
    db.book_seat(ticket)
    ticket = Ticket('2', 1, 'economic', 1, 2)

    with pytest.raises(ChosenSeatIsOccupied):
        db.book_seat(ticket)


def test_database_book_business_seat_number_larger_than_available():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    ticket = Ticket('1', 1, 'business', 1, 2)
    db.book_seat(ticket)
    ticket = Ticket('2', 1, 'business', 1000, 2)

    with pytest.raises(InvalidSeatNumber):
        db.book_seat(ticket)


def test_database_book_economic_seat_number_larger_than_available():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    ticket = Ticket('1', 1, 'economic', 1, 2)
    db.book_seat(ticket)
    ticket = Ticket('2', 1, 'economic', 1000, 2)

    with pytest.raises(InvalidSeatNumber):
        db.book_seat(ticket)


def test_database_release_seat_business():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.release_seat(db.tickets()['1'])
    assert db.planes()[1].business_seats_occupancy()[1] == 'FREE'


def test_database_release_seat_economic():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.release_seat(db.tickets()['5'])
    assert db.planes()[1].economic_seats_occupancy()[1] == 'FREE'


def test_database_release_seat_larger_than_maximum():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    invalid_ticket = Ticket('11', 1, 'business', 500, 1)
    with pytest.raises(InvalidSeatNumber):
        db.release_seat(invalid_ticket)


def test_database_book_seat_larger_than_maximum():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    invalid_ticket = Ticket('11', 1, 'business', 500, 1)
    with pytest.raises(InvalidSeatNumber):
        db.book_seat(invalid_ticket)


def test_database_ask_for_assistance_valid():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')

    db.ask_for_assistance(db.tickets()['1'])
    db.ask_for_assistance(db.tickets()['2'])
    db.ask_for_assistance(db.tickets()['3'])
    assert len(db.planes()[1].busy_assistnats()) == 3


def test_database_ask_for_assistance_more_than_3_passengers_scenario():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')

    db.ask_for_assistance(db.tickets()['1'])
    db.ask_for_assistance(db.tickets()['2'])
    db.ask_for_assistance(db.tickets()['4'])
    assert len(db.planes()[1].busy_assistnats()) == 3

    with pytest.raises(AllAssistantsAreBusyError):
        db.ask_for_assistance(db.tickets()['3'])


def test_database_thank_for_assistance_valid():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')

    db.ask_for_assistance(db.tickets()['1'])
    db.ask_for_assistance(db.tickets()['2'])
    db.ask_for_assistance(db.tickets()['3'])
    assert len(db.planes()[1].busy_assistnats()) == 3

    db.thank_for_assistance(db.tickets()['1'])
    db.thank_for_assistance(db.tickets()['2'])
    db.thank_for_assistance(db.tickets()['3'])
    assert len(db.planes()[1].busy_assistnats()) == 0


def test_database_thank_for_assistance_not_added_passenger():
    db = Database()
    db.read_flights('flights_database.csv')
    db.read_planes('planes_database.csv')
    db.read_tickets('tickets_database.csv')
    db.read_passengers('passengers_database.csv')

    db.ask_for_assistance(db.tickets()['1'])
    db.ask_for_assistance(db.tickets()['2'])
    db.ask_for_assistance(db.tickets()['3'])
    assert len(db.planes()[1].busy_assistnats()) == 3

    db.thank_for_assistance(db.tickets()['1'])
    db.thank_for_assistance(db.tickets()['2'])
    assert len(db.planes()[1].busy_assistnats()) == 1

    with pytest.raises(ChosenPassengerHasNotAskedForHelp):
        db.thank_for_assistance(db.tickets()['4'])
    assert len(db.planes()[1].busy_assistnats()) == 1

    db.thank_for_assistance(db.tickets()['3'])
    assert len(db.planes()[1].busy_assistnats()) == 0

    with pytest.raises(ChosenPassengerHasNotAskedForHelp):
        db.thank_for_assistance(db.tickets()['1'])
    assert len(db.planes()[1].busy_assistnats()) == 0


def test_database_add_plane_lacking_flights():
    db = Database()
    invalid_rows = db.read_planes('planes_database.csv')
    assert invalid_rows == 10


def test_database_add_ticket_lacking_flights():
    db = Database()
    invalid_rows = db.read_tickets('tickets_database.csv')
    assert invalid_rows == 10


def test_database_add_passenger_lacking_tickets():
    db = Database()
    invalid_rows = db.read_passengers('passengers_database.csv')
    assert invalid_rows == 10
