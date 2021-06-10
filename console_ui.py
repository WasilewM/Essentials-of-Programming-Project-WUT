from database import Database
import argparse
import sys


def load_data(database):
    """
    Loads default data into the Database.
    """
    database.read_flights('flights_database.csv')
    database.read_planes('planes_database.csv')
    database.read_tickets('tickets_database.csv')
    database.read_passengers('passengers_database.csv')


def create_table(data):
    """
    Creates table to properly present the data.
    """
    column_width = 0
    for key in data:
        value = data[key]
        column_width = max(
            column_width,
            len(str(key)) + 2,
            len(str(value)) + 2
            )
    horizontal_frame = "-" * (2 * column_width + 2) + '\n'
    result = horizontal_frame
    for key in data:
        value = data[key]
        result += '| ' + f'{key}'
        result += ' ' * (column_width - len(str(key)) - 1)
        snd_column = ' |\n'
        snd_column = f'{value}' + snd_column
        spaces_num = column_width - len(snd_column) + 1
        snd_column = '|' + ' ' * (spaces_num) + snd_column
        result += snd_column
        result += horizontal_frame
    return result


def get_boarding_pass(database, args):
    """
    Prepares the data that will be presented to the user.
    """
    asked_ticket = database.tickets()[args.id]
    asked_person = database.passengers()[args.id]
    table_data = {
        'ticket id': asked_ticket.ticket_id(),
        'first name': asked_person.first_name(),
        'last name': asked_person.last_name(),
        'plane number': asked_ticket.plane_number(),
        'seat class': asked_ticket.seat_class(),
        'seat number': asked_ticket.seat_number(),
        'gate number': asked_ticket.gate_number(),
    }
    table = create_table(table_data)
    print(table)


def get_flights_params(database, args):
    """
    Prepares the data that will be presented to the user.
    """
    asked_plane = database.planes()[int(args.id)]
    business_seats_num = asked_plane.business_seats_number()
    economic_seats_num = asked_plane.economic_seats_number()
    total_seats_num = business_seats_num + economic_seats_num
    if total_seats_num <= 100:
        plane_type = 'continental'
    elif total_seats_num <= 200:
        plane_type = 'narrow-body'
    else:
        plane_type = 'wide-body'
    table_data = {
        'fligths number': asked_plane.plane_number(),
        'plane type': plane_type,
        'number of business class seats': business_seats_num,
        'number of economic class seats': economic_seats_num,
        'carrier name': asked_plane.carrier()
    }
    table = create_table(table_data)
    print(table)


def get_departure_gate(database, args):
    """
    Prepares the data that will be presented to the user.
    """
    gate = database.tickets()[args.id].gate_number()
    table_data = {'gate number': gate}
    table = create_table(table_data)
    print(table)


operation_desc = 'accepts values: flights, planes, tickets, passengers, '
operation_desc += 'boarding_pass, flight_params, check_gate - '
operation_desc += 'values have to be lowercase'

id_desc = 'accepts values (usually ints) if they exist in the Database - \n'
id_desc += 'argument is required in order to specify the object, eg. ticket'


def main(arguments):
    """
    Main funcion of the console_ui.
    """
    database = Database()
    load_data(database)

    parser = argparse.ArgumentParser()
    parser.add_argument('OPERATION', help=operation_desc)
    parser.add_argument('--id', help=id_desc)
    args = parser.parse_args(arguments[1:])

    if args.id:
        if int(args.id) <= 10:
            if args.OPERATION == 'flights':
                print(str(database.flights()[int(args.id)]))
            elif args.OPERATION == 'planes':
                print(str(database.planes()[int(args.id)]))
            elif args.OPERATION == 'tickets':
                print(str(database.tickets()[args.id]))
            elif args.OPERATION == 'passengers':
                print(str(database.passengers()[args.id]))
            elif args.OPERATION == 'boarding_pass':
                get_boarding_pass(database, args)
            elif args.OPERATION == 'flight_params':
                get_flights_params(database, args)
            elif args.OPERATION == 'check_gate':
                get_departure_gate(database, args)
            else:
                print('unknown argument')
        else:
            print('invalid id')
    else:
        if args.OPERATION == 'flights':
            for flight in database.flights():
                print(str(database.flights()[flight]))
        elif args.OPERATION == 'planes':
            for plane in database.flights():
                print(str(database.planes()[plane]))
        elif args.OPERATION == 'tickets':
            for ticket in database.tickets():
                print(str(database.tickets()[ticket]))
        elif args.OPERATION == 'passengers':
            for person in database.passengers():
                print(str(database.passengers()[person]))
        else:
            print('unknown argument')


if __name__ == "__main__":
    main(sys.argv)
