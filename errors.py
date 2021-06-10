class FilePathNotFoundError(FileExistsError):
    pass


class FileIsADirectoryError(IsADirectoryError):
    pass


class InvalidPlaneNumber(Exception):
    pass


class InvalidPassengerName(Exception):
    pass


class InvalidPassengerFirstName(InvalidPassengerName):
    pass


class InvalidPassengerLastName(InvalidPassengerName):
    pass


class InvalidPassengerTicketID(Exception):
    pass


class InvalidNumberOfSeats(Exception):
    pass


class InvalidCarrierName(Exception):
    pass


class InvalidTicketIDNumber(Exception):
    pass


class InvalidSeatNumber(Exception):
    pass


class InvalidGateNumber(Exception):
    pass


class InvalidSeatClass(Exception):
    pass


class InvalidKeyInFlightsFile(KeyError):
    pass


class MalformedFilghtsDataInFile:
    pass


class InvalidKeyInPassengersFile(KeyError):
    pass


class InvalidKeyInPlanesFile(KeyError):
    pass


class InvalidKeyInTicketsFile(KeyError):
    pass


class InvalidInputValueError(ValueError):
    pass


class ChosenSeatIsOccupied(Exception):
    pass


class InvalidTicketDataInput(Exception):
    pass


class LackingTicketObjectError(Exception):
    pass


class LackingFlightObjectError(Exception):
    pass


class InvalidFileHeaderError(Exception):
    pass


class PassengerAlreadyAskedForHelpError(Exception):
    pass


class AllAssistantsAreBusyError(Exception):
    pass


class ChosenPassengerDoesNotExist(Exception):
    pass


class ChosenPassengerHasNotAskedForHelp(Exception):
    pass


class MalformedFileError(Exception):
    pass
