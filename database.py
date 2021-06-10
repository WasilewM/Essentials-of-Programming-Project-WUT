from flight_io import read_flights_from_csv
from passenger_io import read_passengers_from_csv
from plane_io import read_planes_from_csv
from ticket_io import read_tickets_from_csv
from errors import (
    FilePathNotFoundError,
    FileIsADirectoryError,
    InvalidKeyInFlightsFile,
    InvalidKeyInPassengersFile,
    InvalidKeyInPlanesFile,
    InvalidKeyInTicketsFile,
    ChosenSeatIsOccupied,
    InvalidSeatNumber,
    LackingTicketObjectError,
    LackingFlightObjectError,
    InvalidFileHeaderError,
    InvalidPassengerTicketID,
    PassengerAlreadyAskedForHelpError,
    AllAssistantsAreBusyError,
    ChosenPassengerDoesNotExist,
    ChosenPassengerHasNotAskedForHelp,
    MalformedFileError
)


class Database:
    """
    Class Database. Contains attributes:
    :param flights: dictionary of flights in database
    :type flights: dict

    :param passengers: dictionary of passengers in database
    :type passengers: dict

    :param planes: dictionary of planes in database
    :type planes: dict

    :param tickets: dictionary of tickets in database
    :type tickets: dict
    """
    def __init__(self):
        """
        Creates instance of Database.
        """
        self._flights = {}
        self._passengers = {}
        self._planes = {}
        self._tickets = {}

    def flights(self):
        """
        Returns dictionary of flights contained in Database.
        """
        return self._flights

    def passengers(self):
        """
        Returns dictionary of passengers contained in Database.
        """
        return self._passengers

    def planes(self):
        """
        Returns dictionary of planes contained in Database.
        """
        return self._planes

    def tickets(self):
        """
        Returns dictionary of tickets contained in Database.
        """
        return self._tickets

    def add_flight(self, new_flight):
        """
        Adds new_flight into dictionary of flights contained in Database.
        """
        detected_existing_keys = 0
        if new_flight.plane_number() not in self.flights():
            self._flights[new_flight.plane_number()] = new_flight
        else:
            detected_existing_keys += 1
        return detected_existing_keys

    def add_passenger(self, new_passenger):
        """
        Adds new_passenger into dictionary of passengers contained in Database.
        """
        detected_existing_keys = 0
        if new_passenger.ticket_id() not in self.passengers():
            if new_passenger.ticket_id() not in self.tickets():
                raise LackingTicketObjectError
            else:
                self._passengers[new_passenger.ticket_id()] = new_passenger
        else:
            detected_existing_keys += 1
        return detected_existing_keys

    def add_plane(self, new_plane):
        """
        Adds new_plane into dictionary of planes contained in Database.
        """
        detected_existing_keys = 0
        if new_plane.plane_number() not in self.planes():
            if new_plane.plane_number() not in self.flights():
                raise LackingFlightObjectError
            else:
                self._planes[new_plane.plane_number()] = new_plane
        else:
            detected_existing_keys += 1
        return detected_existing_keys

    def book_seat(self, used_ticket):
        """
        Checks whether the seat from used_ticket is available.
        If so, books it, otherwise, informs user that operation
        cannot be done.
        """
        if used_ticket.seat_class() == 'business':
            plane = used_ticket.plane_number()
            plane = self.planes()[plane]
            seat_num = used_ticket.seat_number()

            if seat_num > plane.business_seats_number():
                raise InvalidSeatNumber

            if plane.business_seats_occupancy()[seat_num] == 'FREE':
                self._tickets[used_ticket.ticket_id()] = used_ticket
                plane.business_seats_occupancy()[seat_num] = 'OCCUPIED'
            else:
                raise ChosenSeatIsOccupied
        else:
            plane = used_ticket.plane_number()
            plane = self.planes()[plane]
            seat_num = used_ticket.seat_number()

            if seat_num > plane.economic_seats_number():
                raise InvalidSeatNumber

            if plane.economic_seats_occupancy()[seat_num] == 'FREE':
                self._tickets[used_ticket.ticket_id()] = used_ticket
                plane.economic_seats_occupancy()[seat_num] = 'OCCUPIED'
            else:
                raise ChosenSeatIsOccupied

    def release_seat(self, used_ticket):
        """
        Releases given ticket's seat.
        """
        if used_ticket.seat_class() == 'business':
            plane = used_ticket.plane_number()
            plane = self.planes()[plane]
            seat_num = used_ticket.seat_number()

            if seat_num > plane.business_seats_number():
                raise InvalidSeatNumber

            plane.business_seats_occupancy()[seat_num] = 'FREE'
        else:
            plane = used_ticket.plane_number()
            plane = self.planes()[plane]
            seat_num = used_ticket.seat_number()

            if seat_num > plane.economic_seats_number():
                raise InvalidSeatNumber

            plane.economic_seats_occupancy()[seat_num] = 'FREE'

    def add_ticket(self, new_ticket):
        """
        Adds new_ticket into dictionary of tickets contained in Database.
        """
        detected_existing_keys = 0
        if new_ticket.ticket_id() not in self.tickets():
            if new_ticket.plane_number() not in self.flights():
                raise LackingFlightObjectError
            else:
                self.book_seat(new_ticket)
        else:
            detected_existing_keys += 1
        return detected_existing_keys

    def ask_for_assistance(self, passenger_ticket):
        """
        Adds new passengers that require help if any assistant is free.
        """
        ticket_id = passenger_ticket.ticket_id()
        plane_num = passenger_ticket.plane_number()
        plane = self.planes()[plane_num]
        if ticket_id in self.tickets():
            if not ticket_id or not str(ticket_id):
                raise InvalidPassengerTicketID
            elif ticket_id in plane.busy_assistnats():
                raise PassengerAlreadyAskedForHelpError
            elif len(plane.busy_assistnats()) < 3:
                plane._busy_assistants.add(ticket_id)
            else:
                raise AllAssistantsAreBusyError
        else:
            raise ChosenPassengerDoesNotExist

    def thank_for_assistance(self, passenger_ticket):
        """
        Removes the passengers that no longer need help.
        """
        ticket_id = passenger_ticket.ticket_id()
        plane_num = passenger_ticket.plane_number()
        plane = self.planes()[plane_num]
        if ticket_id in self.tickets():
            if not ticket_id or not str(ticket_id):
                raise InvalidPassengerTicketID
            elif ticket_id not in plane.busy_assistnats():
                raise ChosenPassengerHasNotAskedForHelp
            else:
                plane._busy_assistants.remove(ticket_id)
        else:
            raise ChosenPassengerDoesNotExist

    def read_flights(self, path):
        """
        Reads data from csv files and adds new obecjts of class Flight
        that are not represented in database.
        """
        detected_existing_keys = 0
        try:
            with open(path, 'r')as file_handle:
                data_from_csv = read_flights_from_csv(file_handle)

            if data_from_csv is None:
                raise MalformedFileError

            for flight_num in data_from_csv:
                flight = data_from_csv[flight_num]
                operation_result = self.add_flight(flight)
                detected_existing_keys += operation_result
        except FileNotFoundError:
            raise FilePathNotFoundError
        except IsADirectoryError:
            raise FileIsADirectoryError
        except InvalidKeyInFlightsFile:
            raise InvalidFileHeaderError
        return detected_existing_keys

    def read_passengers(self, path):
        """
        Reads data from csv files and adds new obecjts of class Passenger
        that are not represented in database.
        """
        detected_invalid_rows = 0
        try:
            with open(path, 'r') as file_handle:
                people_from_csv = read_passengers_from_csv(file_handle)

            if people_from_csv is None:
                raise MalformedFileError

            for person_id in people_from_csv:
                try:
                    person = people_from_csv[person_id]
                    operation_result = self.add_passenger(person)
                    detected_invalid_rows += operation_result
                except LackingTicketObjectError:
                    detected_invalid_rows += 1
        except FileNotFoundError:
            raise FilePathNotFoundError
        except IsADirectoryError:
            raise FileIsADirectoryError
        except InvalidKeyInPassengersFile:
            raise InvalidFileHeaderError
        return detected_invalid_rows

    def read_planes(self, path):
        """
        Reads data from csv files and adds new obecjts of class Plane
        that are not represented in database.
        """
        detected_invalid_rows = 0
        try:
            with open(path, 'r') as file_handle:
                planes_from_csv = read_planes_from_csv(file_handle)

            if planes_from_csv is None:
                raise MalformedFileError

            for plane_number in planes_from_csv:
                try:
                    operation_result = self.add_plane(
                        planes_from_csv[plane_number]
                    )
                    detected_invalid_rows += operation_result
                except LackingFlightObjectError:
                    detected_invalid_rows += 1
        except FileNotFoundError:
            raise FilePathNotFoundError
        except IsADirectoryError:
            raise FileIsADirectoryError
        except InvalidKeyInPlanesFile:
            raise InvalidFileHeaderError
        return detected_invalid_rows

    def read_tickets(self, path):
        """
        Reads data from csv files and adds new obecjts of class Tickets
        that are not represented in database.
        """
        detected_invalid_rows = 0
        try:
            with open(path, 'r') as file_handle:
                tickets_from_csv = read_tickets_from_csv(file_handle)

            if tickets_from_csv is None:
                raise MalformedFileError

            for ticket_id in tickets_from_csv:
                try:
                    operation_result = self.add_ticket(
                        tickets_from_csv[ticket_id]
                        )
                    detected_invalid_rows += operation_result
                except (ChosenSeatIsOccupied, LackingFlightObjectError):
                    detected_invalid_rows += 1
        except FileNotFoundError:
            raise FilePathNotFoundError
        except IsADirectoryError:
            raise FileIsADirectoryError
        except InvalidKeyInTicketsFile:
            raise InvalidFileHeaderError
        return detected_invalid_rows
