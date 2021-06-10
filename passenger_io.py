from passenger import Passenger
import csv
from errors import (
    InvalidPassengerFirstName,
    InvalidPassengerLastName,
    InvalidPassengerTicketID,
    InvalidKeyInPassengersFile
)


def read_passengers_from_csv(file_handle, passengers=None):
    """
    Reads data describing objects of class Passenger from csv file.
    Omits invalid data rows.
    """
    if passengers is None:
        passengers = {}
    reader = csv.DictReader(file_handle)
    try:
        for person in reader:
            try:
                first_name = person['first_name']
                last_name = person['last_name']
                ID = person['ticket_id']
                passengers[ID] = Passenger(first_name, last_name, ID)
            except (
                InvalidPassengerFirstName,
                InvalidPassengerLastName,
                InvalidPassengerTicketID
            ):
                continue
    except KeyError:
        raise InvalidKeyInPassengersFile
    except csv.Error:
        return None
    return passengers
