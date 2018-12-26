from werkzeug.security import safe_str_cmp
from user import User

# users indexek nélkül
users = [
    User(1, 'attila', 'teszt'),
    User(2, 'user2', 'abcxyz'),
]

# username_table = {u.username: u for u in users}
# userid_table = {u.id: u for u in users}

# az alábbi mappingelés
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


# users = [
#     {
#         'id': 1,
#         'username': 'Elek',
#         'password': 'qwer',
#     }
# ]

# username_mapping = {'bob': {
#     'id': 1,
#     'username': 'Elek',
#     'password': 'qwer',
# }
# }
#
# userid_mapping = {1: {
#     'id': 1,
#     'username': 'Elek',
#     'password': 'qwer',
# }
# }


# !! ezek átkerülnek a securittyba

def authenticate(username, password):
    user = username_mapping.get(username, None)
    # safe_str_cmp a és b összehasonlítása
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)
