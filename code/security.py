import hmac
import warnings
from resources.user import UserModel
users = [
    UserModel(1, 'bob', 'qwe')
]


username_mapping = {u.username: u for u in users }

userid_mapping = {u.id: u for u in users}

# the following should have been imported from: from werkzeug.security import safe_str_cmp
# but the support ceased since werkzeug==2.0.1 
def safe_str_cmp(a: str, b: str) -> bool:
    """This function compares strings in somewhat constant time.  This
    requires that the length of at least one string is known in advance.
    Returns `True` if the two strings are equal, or `False` if they are not.
    .. deprecated:: 2.0
        Will be removed in Werkzeug 2.1. Use
        :func:`hmac.compare_digest` instead.
    .. versionadded:: 0.7
    """
    warnings.warn(
        "'safe_str_cmp' is deprecated and will be removed in Werkzeug"
        " 2.1. Use 'hmac.compare_digest' instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    if isinstance(a, str):
        a = a.encode("utf-8")  # type: ignore

    if isinstance(b, str):
        b = b.encode("utf-8")  # type: ignore

    return hmac.compare_digest(a, b)

def authenticate(username, password):
    # user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password): # if user and passowrd exists then return the user oject
        return user


def identity(payload):
    user_id = payload['identity']
    # user = userid_mapping.get(user_id, None)           # find if a user with such an id exists and return user object or none
    user = UserModel.find_by_id(user_id)
    return user