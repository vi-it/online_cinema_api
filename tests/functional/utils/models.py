from pydantic import BaseModel


class HTTPResponse(BaseModel):
    body: dict | list[dict]
    headers: dict
    status: int
