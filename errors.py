class Error(Exception):
    """Base class for all exceptions"""
    pass

class PartyInElectionError(Error):
    """Raised when a party is already part of an election"""
    pass

class InvalidCSVFileError(Error):
    """Raised when there is a badly formatted CSV file"""
    pass

class InvalidInputError(Error):
    """Raised when there is a badly formatted CSV file"""
    pass

class InvalidKeyError(Error):
    """Raised when key does not exist in a dictionary"""
    pass