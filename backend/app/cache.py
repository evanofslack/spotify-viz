class Cache:
    auths: dict = {}  # Ongoing authorisations: state -> UserAuth
    users: dict = {}  # User tokens: state -> token (use state as a user ID)


cache = Cache()
