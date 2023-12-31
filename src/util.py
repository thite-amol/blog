"""General purpose module to host common functions."""

from typing import Any, Optional, Union


def generate_response(
    data: Optional[Any] = None,
    message: Optional[Union[dict, list, str]] = None,
    status: Optional[int] = 400,
) -> tuple:
    """It takes in a data, message, and status,
    and returns a dictionary with the data, message, and status.

    Args:
        data (Any): The data that you want to send back to the client.
        message (Optional[Union[dict, list, str]]): his is the message that you want to display to the user
        status (int): The HTTP status code, defaults to 400 (optional)

    Returns:
        tuple: A tuple of a dictionary with the keys: data, message, status.
    """
    status_bool = bool(status == 200 or status == 201)

    return (
        {
            "data": data,
            "message": modify_error(message, status_bool),
            "status": status_bool,
        },
        status,
    )


def modify_error(message: Union[dict, list, str], status: int) -> list:
    """It takes a message and a status, and returns a list of errors.

    Args:
        message (Optional[Union[dict, list, str]]): The error message that you want to display
        status (int): The HTTP status code you want to return

    Returns:
        list: A list of dictionaries.
    """
    final_error = []
    if message:
        if isinstance(message, str):
            if not status:
                final_error.append({"error": message})
            else:
                final_error = message
        elif isinstance(message, list):
            final_error = message
        else:
            for key, value in message.items():
                final_error.append({"error": str(key) + ": " + str(value[0])})

    return final_error
