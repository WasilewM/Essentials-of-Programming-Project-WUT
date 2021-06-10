from database import Database
from flight import Flight
from passenger import Passenger
from plane import Plane
from ticket import Ticket
from errors import (
    InvalidPlaneNumber,
    InvalidPassengerFirstName,
    InvalidPassengerLastName,
    InvalidPassengerTicketID,
    InvalidTicketIDNumber,
    InvalidNumberOfSeats,
    InvalidSeatClass,
    InvalidGateNumber,
    InvalidCarrierName,
    InvalidSeatNumber,
    ChosenSeatIsOccupied,
    InvalidTicketDataInput,
    LackingTicketObjectError,
    LackingFlightObjectError,
    InvalidFileHeaderError,
    PassengerAlreadyAskedForHelpError,
    AllAssistantsAreBusyError,
    ChosenPassengerDoesNotExist,
    ChosenPassengerHasNotAskedForHelp,
    MalformedFileError,
    FileIsADirectoryError,
    FilePathNotFoundError
)


class UserInterface:
    """
    Class UserInterface - responsible for user servicing.
    Contains attributes:
    :param _database: database of the program
    :type _database: class Database

    :param _default_files: dictionary of prepared exemplary files
    :type _default_file: dict

    :param _main_menu: program's main menu options
    :type _main_menu: dict
    """
    def __init__(self):
        """
        Creates instance of UserInterface.
        """
        self._database = Database()
        self._default_files = {
            'flights': 'flights_database.csv',
            'passengers': 'passengers_database.csv',
            'planes': 'planes_database.csv',
            'tickets': 'tickets_database.csv'
        }
        self._main_menu = {
            '0': 'Add data from predefined files',
            '1': 'Add new flight',
            '2': 'Add new plane',
            '3': 'Add new ticket',
            '4': 'Add new passenger',
            '5': 'Show existing flights',
            '6': 'Show existing planes',
            '7': 'Show existing tickets',
            '8': 'Show existing passengers',
            '9': 'Print boarding pass',
            '10': 'Change passenger seat',
            '11': 'Ask for assistant',
            '12': 'Thank assistant for help',
            '13': 'Check departure gate',
            '14': 'Check flight parameters',
            '15': 'Exit'
        }
        self._run()

    def database(self):
        """
        Returns the database of the UI.
        """
        return self._database

    def default_files(self):
        """
        Returns dictionary of deafault data files for objects of classes
        Flight, Passenger, Plane, Ticket.
        """
        return self._default_files

    def main_menu(self):
        """
        Reutrns dictionary of main menu options.
        """
        return self._main_menu

    def greet_the_user(self):
        """
        Greets the user.
        """
        self.show("Hello there!")

    def get_user_input_str(self):
        """
        Takes user input and returns it as str.
        """
        user_input = str(input())
        return user_input

    def get_user_input_int(self):
        """
        Takes user input and returns it as str.
        """
        user_input = int(input())
        return user_input

    def get_main_menu_options(self):
        """
        Returns main menu options as str.
        """
        max_option = len(self.main_menu()) - 1
        options = f'Choose option - type number 0-{max_option}\n'
        for key in self.main_menu():
            row = f'{key}. {self.main_menu()[key]}\n'
            options += row
        options += 'If you want to close the program'
        options += ' instantly please enter Ctrl + D'
        return options

    def show(self, message):
        """
        Displays message on user's screen.
        """
        print(message)

    def handle_invalid_header(self):
        """
        Informs the user about the invalid file header.
        """
        msg = 'Flights data cannot be read due to invalid header in file.\n'
        self.show(msg)
        return False

    def handle_lacking_flights(self):
        """
        Informs the user that data cannot be added into Database due to the
        lack of the data about Flights.
        """
        msg = 'Detected invalid data - data cannot be added into Database.\n'
        msg += 'It is highly probable that one of the following reasons '
        msg += 'creates a problem:\n'
        msg += '1) In order to create a Plane or a Ticket with a specific '
        msg += 'plane number\n'
        msg += 'the Flight with this plane number must be added firstly.\n'
        msg += '2) Chosen seat is occupied.\n'
        msg += '3) Chosen key - plane number or ticket id already exists '
        msg += 'in the Database.\n'
        self.show(msg)
        return False

    def handle_lacking_tickets(self):
        """
        Informs the user that data cannot be added into Database due to the
        lack of the data about Tickets.
        """
        msg = 'Data cannot be added into Database.\n'
        msg = 'Detected invalid data - data cannot be added into Database.\n'
        msg += 'It is highly probable that one of the following reasons '
        msg += 'creates a problem:\n'
        msg += '1) In order to create a Passenger a Ticket for her/him must be'
        msg += 'created firstly.\n'
        msg += '2) A Passenger with chosen ticket id already exists in the '
        msg += 'Database.\n'
        self.show(msg)
        return False

    def invalid_seat_choice(self):
        """
        Creates a message to inform the user about invalid seat number choice.
        """
        msg = 'Invalid seat number.\n'
        msg += 'If you want to get more information about chosen plane, \n'
        msg += 'You can always use option '
        msg += '"Show existing planes" in main menu.\n'
        self.show(msg)

    def handle_occupied_seat(self):
        """
        Creates a message to informa the user about the fact that chosen is
        already occupied and cannot be occupied this time.
        """
        msg = 'Chosen seat is occupied.\n'
        msg += 'Please choose another seat.\n'
        self.show(msg)

    def handle_malformed_file_data(self):
        """
        Creates a message to inform the user about the fact that file cannot
        be read.
        """
        self.show('Critical error ocurred - file cannot be read.\n')

    def handle_file_not_found(self, given_file):
        """
        Creates a message to inform the user that given default file cannot
        be found.
        """
        self.show(f'File: {given_file} cannot be found.')

    def handle_file_is_a_directory(self, given_file):
        """
        Creates a message to inform the user that given default file is a
        directory.
        """
        self.show(f'File: {given_file} is a directory.')

    def load_flights(self):
        """
        Loads Flight data from the default file.
        """
        try:
            result = self.database().read_flights(
                self.default_files()['flights']
            )
            if result:
                msg = f'{result} flights data rows omitted due to detected '
                msg += 'already existing keys.'
                self.show(msg)
                return False
        except InvalidFileHeaderError:
            return self.handle_invalid_header()
        except MalformedFileError:
            return self.handle_malformed_file_data()
        except FilePathNotFoundError:
            return self.handle_file_not_found(self.default_files()['flights'])
        except FileIsADirectoryError:
            return self.handle_file_is_a_directory(
                self.default_files()['flights']
            )
        return True

    def load_planes(self):
        """
        Loads Plane data from the default file.
        """
        try:
            result = self.database().read_planes(
                self.default_files()['planes']
            )
            if result:
                msg = f'{result} planes data rows omitted due to detected '
                msg += 'already existing keys.'
                self.show(msg)
                return False
        except InvalidFileHeaderError:
            return self.handle_invalid_header()
        except LackingFlightObjectError:
            return self.handle_lacking_flights()
        except MalformedFileError:
            return self.handle_malformed_file_data()
        except FilePathNotFoundError:
            return self.handle_file_not_found(self.default_files()['planes'])
        except FileIsADirectoryError:
            return self.handle_file_is_a_directory(
                self.default_files()['planes']
            )
        return True

    def load_tickets(self):
        """
        Loads Tickets data from the default file.
        """
        try:
            result = self.database().read_tickets(
                self.default_files()['tickets']
            )
            if result:
                msg = f'{result} tickets data rows omitted due to detected '
                msg += 'already existing keys.'
                self.show(msg)
                return False
        except InvalidFileHeaderError:
            return self.handle_invalid_header()
        except LackingFlightObjectError:
            return self.handle_lacking_flights()
        except InvalidSeatNumber:
            self.invalid_seat_choice()
        except ChosenSeatIsOccupied:
            self.handle_occupied_seat()
        except MalformedFileError:
            return self.handle_malformed_file_data()
        except FilePathNotFoundError:
            return self.handle_file_not_found(self.default_files()['tickets'])
        except FileIsADirectoryError:
            return self.handle_file_is_a_directory(
                self.default_files()['tickets']
            )
        return True

    def load_passengers(self):
        """
        Loads Passengers data from the default file.
        """
        try:
            result = self.database().read_passengers(
                self.default_files()['passengers']
            )
            if result:
                msg = f'{result} passengers data rows omitted due to detected '
                msg += 'already existing keys.'
                self.show(msg)
                return False
        except InvalidFileHeaderError:
            return self.handle_invalid_header()
        except LackingTicketObjectError:
            return self.handle_lacking_tickets()
        except MalformedFileError:
            return self.handle_malformed_file_data()
        except FilePathNotFoundError:
            return self.handle_file_not_found(
                self.default_files()['passengers']
            )
        except FileIsADirectoryError:
            return self.handle_file_is_a_directory(
                self.default_files()['passengers']
            )
        return True

    def load_default_files(self):
        """
        Manages the process of loading default from dictionary of deafault data
        files for objects of classes Flight, Passenger, Plane, Ticket.
        """
        loaded_flights = self.load_flights()
        loaded_planes = self.load_planes()
        loaded_tickets = self.load_tickets()
        loaded_passengers = self.load_passengers()

        if (loaded_flights is True and loaded_planes is True and
                loaded_tickets is True and loaded_passengers is True):
            self.show('Database loaded successfully.\n')
        else:
            self.show('\n')

    def collect_data_to_create_flight(self):
        """
        Collects data needed in order to create object of class Flight.
        """
        try:
            self.show('Enter plane number: ')
            plane_number = self.get_user_input_int()
            """
            Checking whether values are valid.
            If not appropriate Exception will be raised and handled.
            """
            Flight(plane_number)
            return plane_number
        except (ValueError, InvalidPlaneNumber):
            self.show('Invalid value.')
        return None

    def collect_data_to_create_passenger(self):
        """
        Collects data needed in order to create object of class Passenger.
        """
        try:
            self.show('Enter passenger\'s first name: ')
            fname = self.get_user_input_str()
            self.show('Enter passenger\'s last name: ')
            lname = self.get_user_input_str()
            self.show('Enter passenger\'s ticket id: ')
            ticket_id = self.get_user_input_str()
            """
            Checking whether values are valid.
            If not appropriate Exception will be raised and handled.
            """
            Passenger(fname, lname, ticket_id)
            return fname, lname, ticket_id
        except ValueError:
            self.show('Invalid value.')
        except InvalidPassengerFirstName:
            self.show('Invalid Passenger first name.')
        except InvalidPassengerLastName:
            self.show('Invalid Passenger last name.')
        except InvalidPassengerTicketID:
            self.show('Invalid Passenger ticket id.')
        return None

    def collect_data_to_create_plane(self):
        """
        Collects data needed in order to create object of class Plane.
        """
        try:
            self.show('Enter plane number: ')
            plane_number = self.get_user_input_int()
            self.show('Enter the number of economy class seats: ')
            economic_seats_num = self.get_user_input_int()
            self.show('Enter the number of business class seats: ')
            business_seats_num = self.get_user_input_int()
            self.show('Enter carrier name: ')
            carrier = self.get_user_input_str()
            """
            Checking whether values are valid.
            If not appropriate Exception will be raised and handled.
            """
            Plane(
                plane_number,
                economic_seats_num,
                business_seats_num,
                carrier
            )
            return (
                plane_number,
                economic_seats_num,
                business_seats_num,
                carrier
            )
        except ValueError:
            self.show('Invalid value.')
        except InvalidPlaneNumber:
            self.show('Invalid plane number.')
        except InvalidNumberOfSeats:
            self.show('Invalid number of seats.')
        except InvalidCarrierName:
            self.show('Invalid carrier name.')
        return None

    def get_seat(self):
        """
        Collects data about the seat - class and number.
        """
        try:
            self.show('Enter seat class - must be economic or business: ')
            seat_class = self.get_user_input_str()
            self.show('Enter seat number: ')
            seat_number = self.get_user_input_int()
            return seat_class, seat_number
        except InvalidSeatNumber:
            self.invalid_seat_choice()
        except InvalidSeatClass:
            self.show('Invalid seat class.')
        return None, None

    def collect_data_to_create_ticket(self):
        """
        Collects data needed in order to create object od class Ticket.
        """
        try:
            self.show('Enter ticket id: ')
            ticket_id = self.get_user_input_str()
            self.show('Enter plane number: ')
            plane_number = self.get_user_input_int()
            seat_class, seat_number = self.get_seat()
            self.show('Enter gate number: ')
            gate_number = self.get_user_input_int()
            """
            Checking whether values are valid.
            If not appropriate Exception will be raised and handled.
            """
            Ticket(
                ticket_id,
                plane_number,
                seat_class,
                seat_number,
                gate_number
            )
            return (
                ticket_id,
                plane_number,
                seat_class,
                seat_number,
                gate_number
            )
        except ValueError:
            self.show('Invalid value.')
        except InvalidTicketIDNumber:
            self.show('Invalid ticket id number.')
        except InvalidPlaneNumber:
            self.show('Invalid plane number.')
        except InvalidSeatClass:
            self.show('Invalid seat class.')
        except InvalidGateNumber:
            self.show('Invalid gate number.')
        except ChosenSeatIsOccupied:
            self.handle_occupied_seat()
        return None

    def get_passenger(self):
        """
        Collects data needed to indentify passenger.
        """
        try:
            self.show('Enter passenger\'s ticket id: ')
            passenger_id = self.get_user_input_str()
            if passenger_id not in self.database().tickets():
                msg = 'Chosen ticket id does not exist in Database.\n'
                self.show(msg)
                return None
            elif passenger_id not in self.database().passengers():
                msg = 'Chosen ticket id does not exist in Database.\n'
                msg = 'Passenger with chosen ticket id does not '
                msg += 'exists in Database.\n'
                self.show(msg)
                return None
            else:
                return passenger_id
        except InvalidPassengerTicketID:
            self.show('Invalid Passenger ticket id.')
        return None

    def create_table(self, data):
        """
        Creates table to properly present data to the user.
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

    def get_boarding_pass(self):
        """
        Manages the process of creating a boarding pass.
        """
        passenger_id = self.get_passenger()
        if passenger_id is not None:
            passenger = self.database().passengers()[passenger_id]
            passenger_ticket = self.database().tickets()[passenger_id]
            boarding_pass = {
                'ticket id': passenger.ticket_id(),
                'first name': passenger.first_name(),
                'last name': passenger.last_name(),
                'plane number': passenger_ticket.plane_number(),
                'seat class': passenger_ticket.seat_class(),
                'seat number': passenger_ticket.seat_number(),
                'gate number': passenger_ticket.gate_number()
            }
            boarding_pass = self.create_table(boarding_pass)
            self.show(boarding_pass)

    def try_to_book_ticket(self):
        """
        Tries to book ticket with collected data.
        Handles the exception when user is trying to book
        occupied seat.
        """
        result = None
        try:
            data = self.collect_data_to_create_ticket()
            if data is None:
                raise InvalidTicketDataInput
            result = self.database().add_ticket(Ticket(*data))
        except ChosenSeatIsOccupied:
            self.handle_occupied_seat()
        except InvalidTicketDataInput:
            msg = 'Invalid data - Ticket cannot be created.\n'
            self.show(msg)
        except InvalidSeatNumber:
            self.invalid_seat_choice()
        except LackingFlightObjectError:
            self.handle_lacking_flights()
        if result:
            msg = 'Ticket with such ticket id already exists '
            msg += 'in the database.\n'
            msg += 'Data describing this ticket will be omitted.\n'
            self.show(msg)

    def try_to_change_seat(self):
        """
        Tries to change selected passenger's seat.
        """
        passenger_id = self.get_passenger()
        if passenger_id is not None:
            new_seat_class, new_seat_number = self.get_seat()
            if new_seat_class is not None and new_seat_number is not None:
                ticket = self.database().tickets()[passenger_id]
                data = (
                    ticket.ticket_id(),
                    ticket.plane_number(),
                    ticket.seat_class(),
                    ticket.seat_number(),
                    ticket.gate_number()
                )
                current_ticket = Ticket(*data)
                ticket.set_seat_class(new_seat_class)
                ticket.set_seat_number(new_seat_number)
                try:
                    self.database().book_seat(ticket)
                except ChosenSeatIsOccupied:
                    msg = 'Chosen seat is already occupied.\n'
                    return self.show(msg)
                except InvalidSeatNumber:
                    return self.invalid_seat_choice()
                self.database().release_seat(current_ticket)
            return self.show('Seat changded successfully.\n')
        return self.show('Something went wrong - seat cannot be changed.\n')

    def try_to_ask_for_assistance(self):
        """
        Manages the process of asking for assistance.
        """
        self.show('Enter Passenger\'s ticket id: ')
        passenger_id = self.get_user_input_str()
        try:
            passenger_ticket = self.database().tickets()[passenger_id]
            self.database().ask_for_assistance(passenger_ticket)
        except KeyError:
            return self.show(
                'Chosen ticket id does not exists in the Database.\n'
            )
        except InvalidPassengerTicketID:
            return self.show('Invalid Passenger ticket id.\n')
        except PassengerAlreadyAskedForHelpError:
            return self.show(
                'Chosen Passenger has already asked for assistance.\n'
            )
        except AllAssistantsAreBusyError:
            return self.show(
                'All assistants are busy now. Please try again later.\n'
            )
        except ChosenPassengerDoesNotExist:
            return self.show(
                'Chosen Passenger does not exists in the Database.\n'
            )
        return self.show(
            'Assistant will take care of the Passenger\'s needs.\n'
        )

    def release_assistant(self):
        """
        Manages the process of releasing the assistants.
        """
        self.show('Enter Passenger\'s ticket id: ')
        try:
            passenger_id = self.get_user_input_str()
            passenger_ticket = self.database().tickets()[passenger_id]
            self.database().thank_for_assistance(passenger_ticket)
        except KeyError:
            return self.show(
                'Chosen ticket id does not exists in the Database.\n'
            )
        except InvalidPassengerTicketID:
            return self.show('Invalid Passenger ticket id.\n')
        except ChosenPassengerHasNotAskedForHelp:
            return self.show('Chosen Passenger has not asked for help.\n')
        except ChosenPassengerDoesNotExist:
            return self.show(
                'Chosen Passenger does not exists in the Database.\n'
            )
        return self.show(
            'Assistant will no longer take care of the Passenger\'s needs.\n'
        )

    def check_departure_gate(self):
        """
        Manages the process of checking deprature gate.
        """
        self.show('Enter Passenger\'s ticket id: ')
        try:
            passenger_id = self.get_user_input_str()
            passenger_ticket = self.database().tickets()[passenger_id]
            data = {'departure gate': passenger_ticket.gate_number()}
            data = self.create_table(data)
            self.show(data)
        except KeyError:
            self.show('Chosen ticket id does not exists in the Database.')

    def check_flight_parameters(self):
        """
        Manages the process of checking departure gate.
        """
        self.show('Enter flight number (plane number): ')
        try:
            flight_number = self.get_user_input_int()
            plane = self.database().planes()[flight_number]
            business_seats_num = plane.business_seats_number()
            economic_seats_num = plane.economic_seats_number()
            carrier = plane.carrier()
            seats_num = business_seats_num + economic_seats_num
            if seats_num <= 100:
                plane_type = 'continental'
            elif seats_num <= 200:
                plane_type = 'narrow-body'
            else:
                plane_type = 'wide-body'
            data = {
                'flight number': flight_number,
                'plane type': plane_type,
                'number of business class seats': business_seats_num,
                'number of economy class seats': economic_seats_num,
                'carrier name': carrier
            }
            data = self.create_table(data)
            self.show(data)
        except KeyError:
            self.show('Chosen flight does not exists in the Database')

    def inform_about_main_menu_status(self, option):
        """
        Informs the user about the status of their action.
        Informs the user which main menu option have they chosen.
        """
        msg = f'\nYou have entered "{self.main_menu()[option]}" option.'
        self.show(msg)

    def get_database_status(self, option):
        """
        Orders the self.show() method to display appropriate informaton
        from the Database.
        """
        if option == '1':
            data = self.database().flights()
            if len(data) == 0:
                self.show('Oh no! Nothing here yet...\n')
            else:
                for plane_num in data:
                    self.show(data[plane_num])
        elif option == '2':
            data = self.database().planes()
            if len(data) == 0:
                self.show('Oh no! Nothing here yet...\n')
            else:
                for plane_num in data:
                    self.show(data[plane_num])
        elif option == '3':
            data = self.database().tickets()
            if len(data) == 0:
                self.show('Oh no! Nothing here yet...\n')
            else:
                for ticket_id in data:
                    self.show(data[ticket_id])
        elif option == '4':
            data = self.database().passengers()
            if len(data) == 0:
                self.show('Oh no! Nothing here yet...\n')
            else:
                for person_ticket_id in data:
                    self.show(data[person_ticket_id])
        else:
            self.show('Something went wrong. Database cannot be displayed.')
        self.show('\n')

    def database_status_after_operation(self, option):
        """
        Calls for the get_database_status() method.
        Informs the user why it is happening.
        """
        self.show('\nDatabase status after operation:')
        self.get_database_status(option)

    def try_to_add_flight(self):
        """
        Manages the process of adding new flight by the user.
        """
        data = self.collect_data_to_create_flight()
        if data is not None:
            result = self.database().add_flight(Flight(data))
            if result:
                msg = 'Flight with such plane number already exists '
                msg += 'in the database.\n'
                msg += 'Data describing this flight will be omitted.\n'
                self.show(msg)

    def try_to_add_plane(self):
        """
        Manages the process of adding new plane by the user.
        """
        try:
            data = self.collect_data_to_create_plane()
            if data is not None:
                result = self.database().add_plane(Plane(*data))
                if result:
                    msg = 'Plane with such plane number already exists '
                    msg += 'in the database.\n'
                    msg += 'Data describing this plane will be omitted.\n'
                    self.show(msg)
        except LackingFlightObjectError:
            self.handle_lacking_flights()

    def try_to_add_passenger(self):
        try:
            data = self.collect_data_to_create_passenger()
            if data is not None:
                result = self.database().add_passenger(Passenger(*data))
                if result:
                    msg = 'Passenger with such ticket id already exists '
                    msg += 'in the database.\n'
                    msg += 'Data describing this passenger will be omitted.\n'
                    self.show(msg)
        except LackingTicketObjectError:
            self.handle_lacking_tickets()

    def menu_choose_user_option(self, option):
        """
        Chooses instraction appropriate for executing user's choice.
        """
        valid_options = {f'{num}' for num in range(0, 15)}

        if option in valid_options:
            self.inform_about_main_menu_status(option)

        if option == '0':
            self.load_default_files()
        elif option == '1':
            self.try_to_add_flight()
            self.database_status_after_operation(option)
        elif option == '2':
            self.try_to_add_plane()
            self.database_status_after_operation(option)
        elif option == '3':
            self.try_to_book_ticket()
            self.database_status_after_operation(option)
        elif option == '4':
            self.try_to_add_passenger()
            self.database_status_after_operation(option)
        elif option == '5':
            self.get_database_status('1')
        elif option == '6':
            self.get_database_status('2')
        elif option == '7':
            self.get_database_status('3')
        elif option == '8':
            self.get_database_status('4')
        elif option == '9':
            self.inform_about_main_menu_status(option)
            self.get_boarding_pass()
        elif option == '10':
            self.try_to_change_seat()
        elif option == '11':
            self.try_to_ask_for_assistance()
        elif option == '12':
            self.release_assistant()
        elif option == '13':
            self.check_departure_gate()
        elif option == '14':
            self.check_flight_parameters()
        elif option == '15':
            self.show('Thank you for using my program. Have a nice day!')
        else:
            self.show('Invalid value. Please try again.')

    def _run(self):
        """
        Main function of the interface - the loop.
        """
        self.greet_the_user()
        end = False
        while not end:
            main_menu = self.get_main_menu_options()
            self.show(main_menu)
            user_choice = self.get_user_input_str()
            self.menu_choose_user_option(user_choice)
            for key in self.main_menu():
                if self.main_menu()[key] == 'Exit':
                    exit_option = key
            if user_choice == exit_option:
                end = True
