import string
from functools import total_ordering
from enum import Enum, unique
from typing import TypeVar, Generic, Final, Type
import uuid_utils as uuid

E = TypeVar("E", bound=Enum)
T = TypeVar("T", bound="BaseID")


@total_ordering
class BaseID(Generic[E]):
    """
    Abstract base class for all ID types. The generic type argument `E`
    should be an `Enum` with members for each distinct ID type in your
    system. The Enum member name can be descriptive (e.g., `ACCOUNT`)
    but the value should be the prefix on all IDs of that type
    (e.g., 'acct'). Use the `enum.unique` decorator to ensure the values
    remain unique.

    Encoded IDs will be in the form:
        `{PREFIX.value}_{base36-encoded-id}`

    The ID portion is currently a UUIDv7, so it is unique across space
    and time, but still provides a natural creation ordering.
    """

    PREFIX_SEPARATOR: Final = "_"
    _ALPHABET: Final = string.digits + string.ascii_lowercase
    _ALPHABET_LEN: Final = len(_ALPHABET)

    PREFIX: E
    """
    PREFIX must be set by derived classes to a member of the enum.
    """
    _id: str

    def __init__(self):
        id_int = uuid.uuid7().int
        encoded_chars = []
        while id_int > 0:
            id_int, remainder = divmod(id_int, self._ALPHABET_LEN)
            encoded_chars.append(self._ALPHABET[remainder])
        self._id = "".join(reversed(encoded_chars))

    def __str__(self) -> str:
        return f"{self.PREFIX.value}{self.PREFIX_SEPARATOR}{self._id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.__str__()}')"

    def __eq__(self, other) -> bool:
        return self._id == other._id if type(self) is type(other) else False

    def __lt__(self, other) -> bool:
        return self._id < other._id if type(self) is type(other) else NotImplemented

    def __hash__(self) -> int:
        return hash(str(self))

    @classmethod
    def parse(cls: Type[T], encoded_id: str) -> T:
        """
        Parses an encoded ID back into an instance of the ID class.
        If the prefix on the encoded ID does not match the declared
        PREFIX, this raises ValueError.
        """
        expected_prefix = cls.PREFIX.value + cls.PREFIX_SEPARATOR
        if not encoded_id.startswith(expected_prefix):
            raise ValueError(
                f"Encoded ID {encoded_id} does not have expected prefix {cls.PREFIX}"
            )
        _, id = encoded_id.split(cls.PREFIX_SEPARATOR, 1)

        obj = cls.__new__(cls)
        obj._id = id
        return obj


@unique
class IDType(Enum):
    """
    Set of ID types in this system. Member values are used
    as the ID prefix, so they must remain unique.
    """

    ACCOUNT = "acct"
    SESSION = "ses"

    @classmethod
    def from_id(cls, encoded_id: str) -> "IDType":
        """
        Returns the IDType from an encoded ID. If the prefix
        of the encoded ID doesn't match any of the Enum members,
        a `ValueError` is raised.
        """
        for member in cls:
            if encoded_id.startswith(member.value + "_"):
                return IDType(member)
        raise ValueError(f"Unknown prefix in ID: '{encoded_id}'")


class ModelID(BaseID[IDType]):
    pass


class AccountID(ModelID):
    PREFIX = IDType.ACCOUNT


class SessionID(ModelID):
    PREFIX = IDType.SESSION


def account_id_func(id: AccountID) -> str:
    return str(id)


def main() -> None:
    id = uuid.uuid7()
    print(repr(id))

    account_id = AccountID()
    session_id = SessionID()
    print(repr(account_id))
    print(account_id)
    print(repr(session_id))
    print(session_id)

    print("some account IDs:")
    for _ in range(10):
        print(AccountID())


if __name__ == "__main__":
    main()
