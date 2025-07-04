class RestaurantException(Exception):
    """Base exception for restaurant module."""
    pass

class RestaurantNotFoundError(RestaurantException):
    """Raised when a restaurant is not found."""
    pass

class RestaurantAlreadyExistsError(RestaurantException):
    """Raised when a restaurant with the same name already exists."""
    pass
    
class TableNumberConflictError(RestaurantException):
    """Raised when a table with the same number already exists in the restaurant."""
    pass

class CannotDeleteRestaurantWithTablesError(RestaurantException):
    """Raised when attempting to delete a restaurant that still has tables."""
    pass
