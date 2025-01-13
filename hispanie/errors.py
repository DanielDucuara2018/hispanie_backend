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


class NoDataFound(Error):
    code = 1000
    reason = "no-data-found"
    description = "No data found in DB."


class NoUserFound(Error):
    code = 1001
    reason = "no-user-found"
    description = "No user found in DB."
