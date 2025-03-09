from typing import Any


class Error(Exception):
    code: int
    reason: str
    description: str

    def __init__(self, **data: Any):
        self.data = data

    def __str__(self):
        fields = [
            ("code", self.code),
            ("reason", self.reason),
            ("data", repr(self.data)),
        ]
        fields_repr = ", ".join(f"{field}={value}" for field, value in fields)
        return fields_repr


class DBError(Error):
    code = 900
    reason = "db-error"
    description = "Error occurred while performing a database action."


class NoDataFound(Error):
    code = 1000
    reason = "no-data-found"
    description = "No data found in DB."


class NoUserFound(Error):
    code = 1001
    reason = "no-user-found"
    description = "No user found in DB."


class NoBusinessFound(Error):
    code = 1002
    reason = "no-business-found"
    description = "No tag found in DB."


class NoEventFound(Error):
    code = 1003
    reason = "no-event-found"
    description = "No tag found in DB."


class NoTagFound(Error):
    code = 1004
    reason = "no-tag-found"
    description = "No tag found in DB."


class NoActivityFound(Error):
    code = 1005
    reason = "no-activity-found"
    description = "No activity found in DB."


class NoTicketFound(Error):
    code = 1006
    reason = "no-ticket-found"
    description = "No ticket found in DB."
