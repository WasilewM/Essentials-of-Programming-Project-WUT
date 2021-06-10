from plane import Plane
import csv
from errors import (
    InvalidPlaneNumber,
    InvalidNumberOfSeats,
    InvalidCarrierName,
    InvalidKeyInPlanesFile
)


def read_planes_from_csv(file_handle):
    """
    Reads data describing objects of class Plane from csv file.
    Omits invalid data rows
    """
    planes = {}
    reader = csv.DictReader(file_handle)
    try:
        for plane in reader:
            try:
                plane_number = int(plane['plane_number'])
                economic_seats_num = int(plane['economic_seats_number'])
                business_seats_num = int(plane['business_seats_number'])
                carrier = plane['carrier']
                planes[plane_number] = Plane(
                    plane_number,
                    economic_seats_num,
                    business_seats_num,
                    carrier
                )
            except (
                InvalidPlaneNumber,
                InvalidNumberOfSeats,
                InvalidCarrierName,
                ValueError
            ):
                continue
    except KeyError:
        raise InvalidKeyInPlanesFile
    except csv.Error:
        return None
    return planes
