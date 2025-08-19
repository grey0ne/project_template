from dataclasses import dataclass


@dataclass(kw_only=True, slots=True, frozen=True)
class UserData:
    id: int
    username: str


@dataclass(kw_only=True, slots=True, frozen=True)
class CurrentUserData:
    id: int
    username: str
    is_superuser: bool | None = None

@dataclass(kw_only=True, slots=True, frozen=True)
class CurrentUserResponse:
    user: CurrentUserData