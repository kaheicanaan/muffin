import enum


class Role(enum.Enum):
    member = "MEMBER"
    owner = "OWNER"
    admin = "ADMIN"
    announcer = "ANNOUNCER"
