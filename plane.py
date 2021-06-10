from flight import Flight
from errors import (
    InvalidNumberOfSeats,
    InvalidCarrierName
)


class Plane(Flight):
    """
    Class Plane. Contains attributes:
    :param plane_nummber: plane's number
    :type plane_number: int

    :param economic_seats_number: plane's number of econonic class seats
    :type economic_seats_number: int

    :param business_seats_number: plane's number of business class seats
    :type business_of_seats: int

    :param carrier: represents plane's carrier name
    :type carrier: str

    :param economic_seats_occupancy: dictionary representing occupancy in
    economy class seats
    :type economic_seats_occupancy: str
    Value must be either 'free' or 'occupied'

    :param business_seats_occupancy: dictionary representing occupancy in
    business class seats
    :type business_seats_occupancy: str
    Value must be either 'FREE' or 'OCCUPIED'

    :param bussy_assistants: set representing passenger's ticket id that
    require help - length of the set represents the number of assistnats
    that are busy
    Maximum number of passengers that can be helped at once is 3
    :type bussy_assistants: set
    """
    def __init__(
        self,
        plane_number,
        economic_seats_num,
        business_seats_num,
        carrier
    ):
        """
        Creates instance of Plane.
        """
        super().__init__(plane_number)
        if self._if_economic_seats_number(economic_seats_num):
            self._economic_seats_number = int(economic_seats_num)
        if self._if_business_seats_number(business_seats_num):
            self._business_seats_number = int(business_seats_num)
        if self._if_carrier(carrier):
            self._carrier = carrier.upper()
        self._economic_seats_occupancy = {
            id: 'FREE'
            for id in range(1, economic_seats_num + 1)
            }
        self._business_seats_occupancy = {
            id: 'FREE'
            for id in range(1, business_seats_num + 1)
            }
        self._busy_assistants = set()

    def _if_economic_seats_number(self, seats_num):
        """
        Checks whether the number of economic class seats is a positive int.
        """
        if not int(seats_num) > 0 or int(seats_num) != seats_num:
            raise InvalidNumberOfSeats
        return True

    def _if_business_seats_number(self, seats_num):
        """
        Checks whether the number of business class seats is a positive int.
        """
        if not int(seats_num) > 0 or int(seats_num) != seats_num:
            raise InvalidNumberOfSeats
        return True

    def _if_carrier(self, carrier):
        """
        Checks whether the carrier is not an empty str.
        Checks also whether the carrier str can be made uppercase.
        """
        if not carrier or not carrier.upper():
            raise InvalidCarrierName
        return True

    def economic_seats_number(self):
        """
        Returns plane's number of economic class seats.
        """
        return self._economic_seats_number

    def business_seats_number(self):
        """
        Returns plane's number of business class seats.
        """
        return self._business_seats_number

    def carrier(self):
        """
        Returns plane's carrier name.
        """
        return self._carrier

    def __str__(self):
        """
        Returns description about the object of class Plane.
        """
        num = self.plane_number()
        economic = self.economic_seats_number()
        business = self.business_seats_number()
        carrier = self.carrier()
        desc = f'Plane: plane number: {num}, economic seats number: {economic}'
        desc += f', business seats number: {business}, carrier: {carrier}'
        return desc

    def economic_seats_occupancy(self):
        """
        Returns dictionary representing occupancy in economy class seats.
        """
        return self._economic_seats_occupancy

    def business_seats_occupancy(self):
        """
        Returns dictionary representing occupancy in business class seats.
        """
        return self._business_seats_occupancy

    def busy_assistnats(self):
        """
        Returns the set of tickets id of the passengers' that require help.
        """
        return self._busy_assistants
