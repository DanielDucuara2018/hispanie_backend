from datetime import datetime

from pydantic import PlainSerializer
from typing_extensions import Annotated

CustomDateTime = Annotated[
    datetime,
    PlainSerializer(lambda _datetime: _datetime.strftime("%Y-%m-%d %H:%M:%S"), return_type=str),
]
