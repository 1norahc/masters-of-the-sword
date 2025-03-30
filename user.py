
import re

class User:

    def __init__(self,
                 first_name,
                 last_name,
                 nickname,
                 email,
                 password):

        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.email = email
        self.password = password

