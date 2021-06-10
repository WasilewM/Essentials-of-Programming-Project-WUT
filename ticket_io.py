from ticket import Ticket
import csv
from errors import (
    InvalidTicketIDNumber,
    InvalidSeatNumber,
    InvalidGateNumber,
    InvalidSeatClass,
    InvalidPlaneNumber,
    InvalidKeyInTicketsFile
)


def read_tickets_from_csv(file_handle):
    """
    Reads data describing objects of class Ticket from csv file.
    Omits invalid data rows.
    """
    tickets = {}
    reader = csv.DictReader(file_handle)
    try:
        for ticket in reader:
            try:
                ticket_id = ticket['ticket_id']
                plane_number = int(ticket['plane_number'])
                seat_class = ticket['seat_class']
                seat_number = int(ticket['seat_number'])
                gate_number = int(ticket['gate_number'])
                tickets[ticket_id] = Ticket(
                    ticket_id,
                    plane_number,
                    seat_class,
                    seat_number,
                    gate_number
                )
            except (
                ValueError,
                InvalidPlaneNumber,
                InvalidSeatClass,
                InvalidSeatNumber,
                InvalidGateNumber,
                InvalidTicketIDNumber
            ):
                continue
    except KeyError:
        raise InvalidKeyInTicketsFile
    except csv.Error:
        return None
    return tickets
