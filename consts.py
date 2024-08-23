"""This file stores a bunch of constant values that are reused throughout the
project, so that they can be easily changed when needed
    """

# Point this to your SQL database file
DATABASE = 'database.db'

# Set this to the URL of your app (this is just used for generating URLs)
URL = 'http://127.0.0.1:5000'

# Secret key used for JWT
APP_SECRET_KEY = b'\xb5p\xab4aB\xe6\xfc\xd2^\xb0\xe7\x16Xr3\x180:\xf4\xae\xd1\t%'

# This is just used for generating things like upload keys - you shouldnt need to
# touch it
CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-_'
