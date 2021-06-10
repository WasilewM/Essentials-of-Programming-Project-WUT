from errors import InvalidPlaneNumber


class Flight:
    """
    Class Flight. Contains attributes:
    :param plane_nummber: plane's number
    :type plane_number: int
    """
    def __init__(self, plane_number):
        """
        Creates instance of class Flight.
        """
        if self._if_plane_number(plane_number):
            self._plane_number = int(plane_number)

    def _if_plane_number(self, plane_number):
        """
        Checks whether the plane_number is a positive integer.
        """
        if not int(plane_number) > 0 or int(plane_number) != plane_number:
            raise InvalidPlaneNumber
        return True

    def plane_number(self):
        """
        Returns plane's number.
        """
        return self._plane_number

    def __str__(self):
        """
        Returns description about the object of class Flight.
        """
        return f'Flight: plane number: {self.plane_number()}'
