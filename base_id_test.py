import pytest
from .base_id import BaseID


class AccountID(BaseID):
    PREFIX = "acct"


class SessionID(BaseID):
    PREFIX = "ses"


def test_creation() -> None:
    assert str(AccountID()).startswith(AccountID.PREFIX + BaseID.PREFIX_SEPARATOR)
    assert str(SessionID()).startswith(SessionID.PREFIX + BaseID.PREFIX_SEPARATOR)


def test_equality() -> None:
    id1 = AccountID()
    id2 = id1
    assert id2 == id1


def test_inequality() -> None:
    id1 = AccountID()
    id2 = AccountID()
    assert id1 != id2


def test_ordering() -> None:
    id1 = AccountID()
    id2 = AccountID()
    assert id2 >= id1
    assert id1 <= id2


def test_init() -> None:
    id = AccountID()
    rehydrated_id = AccountID(id)
    assert type(rehydrated_id) is AccountID
    assert rehydrated_id == id


def test_init_fail() -> None:
    acct_id = AccountID()
    ses_id = SessionID()
    with pytest.raises(ValueError):
        SessionID(acct_id)
    with pytest.raises(ValueError):
        AccountID(ses_id)


def test_parse() -> None:
    id = AccountID()
    parsed_id = BaseID.parse(id)
    assert type(parsed_id) is AccountID
    assert parsed_id == id


def test_parse_fail() -> None:
    with pytest.raises(ValueError):
        BaseID.parse("invalid_123")


def test_create_base_fail() -> None:
    with pytest.raises(AttributeError):
        BaseID()


def test_define_duplicate_prefix_fail() -> None:
    prefix = "test"
    if prefix in BaseID.prefix_to_class_map:
        del BaseID.prefix_to_class_map[prefix]

    class TestID(BaseID):
        PREFIX = prefix

    with pytest.raises(ValueError):

        class DuplicatePrefixID(BaseID):
            PREFIX = prefix


def test_new_random() -> None:
    class MeetingID(BaseID):
        PREFIX = "meet"
        ORDERED = False

    id = MeetingID()
    assert id.startswith(MeetingID.PREFIX)
