from errors import (
    InvalidPassengerFirstName,
    InvalidPassengerLastName,
    InvalidPassengerTicketID
)


class Passenger:
    """
    Class Passenger. Contains attributes:
    :param first_name: passenger's first name
    :type first_name: str

    :param last_name: passenger's last name
    :type last_name: str

    :param ticket_id: passenger's ticket id
    :type ticket_id: str
    """
    def __init__(self, fname, lname, ticket_id):
        """
        Creates instance of passenger.
        """
        if self._if_fname(fname):
            self._first_name = str(fname)
        if self._if_lname(lname):
            self._last_name = str(lname)
        if self._if_ticket_id(ticket_id):
            self._ticket_id = str(ticket_id)

    def _if_fname(self, fname):
        """
        Checks whether the first name is a not empty string.
        """
        if not fname or not str(fname):
            raise InvalidPassengerFirstName
        return True

    def _if_lname(self, lname):
        """
        Checks whether the last name is a not empty string.
        """
        if not lname or not str(lname):
            raise InvalidPassengerLastName
        return True

    def _if_ticket_id(self, ticket_id):
        """
        Checks whether the ticket_id is a not empty string.
        """
        if not ticket_id or not str(ticket_id):
            raise InvalidPassengerTicketID
        return True

    def first_name(self):
        """
        Returns passenger's first name.
        """
        return self._first_name

    def last_name(self):
        """
        Returns passenger's last name.
        """
        return self._last_name

    def ticket_id(self):
        """
        Returns passenger's ticket id.
        """
        return self._ticket_id

    def __str__(self):
        """
        Returns description about the object of class Passenger.
        """
        fname = self.first_name()
        lname = self.last_name()
        ID = self.ticket_id()
        description = f'Passenger: {fname} {lname}, ticket id number: {ID}'
        return description
