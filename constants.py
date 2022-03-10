from enum import Enum


class OutPutMessages:
    start_message = "Oww!hi"
    about_us = "We can merge pdf files for you:)"


class UserState(Enum):
    DONE = 1
    WAITING_TO_RECEIVE_PDF_FILE = 2
