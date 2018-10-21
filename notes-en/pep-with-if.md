
## Syntax

```python
with manager [as alias] if condition:
  ...
```

## Example

For example, we have function for getting users from database.
1. If session is passed to function then use it, but don't close.
2. If there is no session passed then create new session and close it after all.

```python
def get_users(session=None):
  with get_session() as session if session is None:
    # do something
    ...
```

Let's look possible solutions without this syntax.

Bad solution:

```python
def get_users(session=None):
  if session is None:
    # do something
    ...
  else:
    with get_session() as session:
      # do the same
      ...
```

DRY solution:

```python
def _get_users(session):
  # do something
  ...

def get_users(session=None):
  if session is None:
    return _get_users(session)
  with get_session(session) as session:
    return _get_users(session)
```

However if function gets many arguments then we should pass them all to new
function in both calls.
