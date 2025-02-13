"""
Utils used by the API for modularity
This file stores utilities of the API in order to modularize the API
 and centralize its resources
"""
import datetime
import json
import logging

import werkzeug

_logger = logging.getLogger(__name__)

# API key that should be received with each request sent to a
# controller decorated with @verify_key
API_KEY = 1234585236
STATUS_SUCCESS = True
STATUS_ERROR = False

# URL prefix used to manipulate the endpoints
URL_PREFIX = "/api"


# Helper method used to return similarly formatted responses from all endpoints
def json_response(res, status, message):
    """
    This function formats responses returned from all endpoints,
     in order to centralize the response formatter
    :param res: The actual result which be used by frontend apps
    :param status: The status of the call; either STATUS_ERROR or STATUS_SUCCESS
    :param message: The message which will be sent to frontend apps
    :return: a dictionary containing all parameters formatted as a json object
    """
    response = {"success": status, "data": res, "message": message}
    # This is for debugging purposes
    _logger.info(response)
    return response


def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, bytes):
        return str(o)


def valid_response(data, status=200):
    """Valid Response This will be return when the http request was successfully processed."""
    data = {
        "count": len(data) if not isinstance(data, str) else 1,
        "status": status,
        "data": data,
    }
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(data, default=default),
    )


def invalid_response(r_type, message=None, status=401):
    """Invalid Response This will be the return value whenever the server runs into an error
    either from the client or the server."""
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(
            {
                "type": r_type,
                "message": str(message)
                if str(message)
                else "Wrong arguments (missing validation)",
            },
            default=datetime.datetime.isoformat,
        ),
    )
