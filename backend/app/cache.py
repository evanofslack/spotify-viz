class Cache:
    auths = {}  # Ongoing authorisations: state -> UserAuth
    users = {}  # User tokens: state -> token (use state as a user ID)


cache = Cache()
