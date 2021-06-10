from flight import Flight
from errors import (
    InvalidTicketIDNumber,
    InvalidSeatNumber,
    InvalidGateNumber,
    InvalidSeatClass
)


class Ticket(Flight):
    """
    Class Ticket. Contains attributes:
    :param ticket_id: ticket id value
    :type ticket_id: str

    # :param plane_number: ticket's owner plane number
    # :type plane_number: int

    :param seat_class: ticket's owner seat class
        has to be either 'business' or 'economic'
    :type seat_class: str

    :param seat_number: ticket's owner seat number
    :type seat_number: int

    :param gate_number: ticket's owner gate number
    :type gate_number: int
    """
    def __init__(
        self,
        ticket_id,
        plane_number,
        seat_class,
        seat_number,
        gate_number
    ):
        """
        Creates instance of Ticket.
        """
        super().__init__(plane_number)
        if self._if_ticket_id(ticket_id):
            self._ticket_id = str(ticket_id)
        self.set_seat_class(seat_class)
        self.set_seat_number(seat_number)
        if self._if_gate_number(gate_number):
            self._gate_number = int(gate_number)

    def _if_ticket_id(self, ticket_id):
        """
        Checks whether the ticket_id is a not empty string.
        """
        if not ticket_id or not str(ticket_id):
            raise InvalidTicketIDNumber
        return True

    def _if_gate_number(self, gate_number):
        """
        Checks whether the gate_number is a positive integer.
        """
        if not int(gate_number) > 0 or int(gate_number) != gate_number:
            raise InvalidGateNumber
        return True

    def set_seat_class(self, seat_class):
        """
        Checks whether the seat class value is either 'business' or 'economic'.
        If so sets new value, otherwise raises InvalidSeatClass exception.
        """
        if seat_class not in {'business', 'economic'}:
            raise InvalidSeatClass
        self._seat_class = seat_class

    def set_seat_number(self, seat_number):
        """
        Checks whether the seat_number is a positive integer.
        If so sets new value, otherwise raises InvalidSeatNumber exception.
        """
        if not int(seat_number) > 0 or int(seat_number) != seat_number:
            raise InvalidSeatNumber
        self._seat_number = int(seat_number)

    def ticket_id(self):
        """
        Returns ticket's id.
        """
        return self._ticket_id

    def seat_class(self):
        """
        Returns ticket's seat class.
        """
        return self._seat_class

    def seat_number(self):
        """
        Returns ticket's seat number.
        """
        return self._seat_number

    def gate_number(self):
        """
        Returns ticket's gate number.
        """
        return self._gate_number

    def __str__(self):
        """
        Returns desrciption about the object of class Ticket.
        """
        ID = self.ticket_id()
        plane_num = self.plane_number()
        seat_class = self.seat_class()
        seat_num = self.seat_number()
        gate_num = self.gate_number()
        desc = f'Ticket: id: {ID}, plane number: {plane_num}, '
        desc += f'seat class: {seat_class}, seat number: {seat_num}, '
        desc += f'gate number: {gate_num}'
        return desc
