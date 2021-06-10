from flight import Flight, InvalidPlaneNumber
import csv
from errors import (
    InvalidKeyInFlightsFile
)


def read_flights_from_csv(file_handle):
    """
    Reads data describing objects of class Flight from csv file.
    Omits invalid data rows.
    """
    flights = {}
    reader = csv.DictReader(file_handle)
    try:
        for flight_number in reader:
            try:
                plane_number = int(flight_number['plane_number'])
                flights[plane_number] = Flight(plane_number)
            except (ValueError, InvalidPlaneNumber):
                continue
    except KeyError:
        raise InvalidKeyInFlightsFile
    except csv.Error:
        return None
    return flights
