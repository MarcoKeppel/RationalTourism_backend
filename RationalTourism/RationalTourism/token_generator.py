import string
import random


def new_token(length=15):
    return ''.join(random.choices(string.ascii_letters, k=length))

