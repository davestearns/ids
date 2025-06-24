import pytest
import time
from main import IDType, AccountID, SessionID, BaseID


def test_creation() -> None:
    assert str(AccountID()).startswith(IDType.ACCOUNT.value + BaseID.PREFIX_SEPARATOR)
    assert str(SessionID()).startswith(IDType.SESSION.value + BaseID.PREFIX_SEPARATOR)


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
    time.sleep(0.2)
    id2 = AccountID()
    assert id2 > id1
    assert id1 < id2


def test_type_from_id() -> None:
    assert IDType.from_id(str(AccountID())) == IDType.ACCOUNT
    assert IDType.from_id(str(SessionID())) == IDType.SESSION


def test_parse() -> None:
    id = AccountID()
    encoded_id = str(id)
    parsed_id = AccountID.parse(encoded_id)
    assert type(parsed_id) is AccountID
    assert parsed_id == id


def test_parse_fail() -> None:
    acct_id = AccountID()
    ses_id = SessionID()
    with pytest.raises(ValueError):
        SessionID.parse(str(acct_id))
    with pytest.raises(ValueError):
        AccountID.parse(str(ses_id))
