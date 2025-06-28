# Application-Assigned IDs

This repo contains example code discussed in my
[application assigned IDs tutorial](https://davestearns.github.io/tutorials/ids.html).

Specifically it contains a
[base class](https://github.com/davestearns/ids/blob/main/base_id.py) you can
use for defining strongly-typed and prefixed IDs in Python. For example:

```python
from base_id import BaseID

class AccountID(BaseID):
    PREFIX = "acct"

class SessionID(BaseID):
    PREFIX = "ses"

account_id = AccountID()
print(account_id) # => acct_3e6wlko0bp8e7c9916hklbnd

# account_id is an AccountID
assert type(account_id) is AccountID

# But it's also just a string,
# so it works anywhere a str does
assert isinstance(account_id, str)

# And SessionID is a different type than AccountID
assert type(AccountID()) is not type(SessionID())

# When you receive one of these IDs as a string,
# you can rehydrate it back into the specific type
# and this will raise ValueError if the ID isn't the
# correct prefix.
id_sent_to_client: str = str(account_id)
rehydrated_account_id = AccountID(id_sent_to_client)
assert type(rehydrated_account_id) is AccountID
assert rehydrated_account_id == account_id

# If you receive one of these IDs as a string, but
# aren't sure what specific type it is, 
# use BaseID.parse() to parse it into the appropriate
# type based on its prefix. This will raise ValueError
# if the prefix doesn't match any of the declared
# prefixes on the various subclasses
unknown_id_typ: str = str(account_id)
parsed_id = BaseID.parse(unknown_id_type)
assert type(parsed_id) is AccountID
```
