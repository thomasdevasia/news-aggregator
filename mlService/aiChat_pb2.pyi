from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class userData(_message.Message):
    __slots__ = ("userName", "heading", "data", "newsDate")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    NEWSDATE_FIELD_NUMBER: _ClassVar[int]
    userName: str
    heading: str
    data: str
    newsDate: str
    def __init__(self, userName: _Optional[str] = ..., heading: _Optional[str] = ..., data: _Optional[str] = ..., newsDate: _Optional[str] = ...) -> None: ...

class SaveToVectorDbResponse(_message.Message):
    __slots__ = ("response", "status")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    response: str
    status: bool
    def __init__(self, response: _Optional[str] = ..., status: bool = ...) -> None: ...

class prompt(_message.Message):
    __slots__ = ("userName", "prompt")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    userName: str
    prompt: str
    def __init__(self, userName: _Optional[str] = ..., prompt: _Optional[str] = ...) -> None: ...

class ChatResponse(_message.Message):
    __slots__ = ("response", "status", "done")
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DONE_FIELD_NUMBER: _ClassVar[int]
    response: str
    status: bool
    done: bool
    def __init__(self, response: _Optional[str] = ..., status: bool = ..., done: bool = ...) -> None: ...
