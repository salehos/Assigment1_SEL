from enum import Enum


class OutPutMessages:
    start_message = "Oww!hi"
    about_us = "We can merge pdf files for you:)"
    pdf_merge_request = "Ok! Now you can send me some pdfs."
    got_it = "Ok! Got it.\n/done ?"
    merging = "Merging ..., wait a sec!"
    no_file = "No file sent to be merged!!! Send them again"


class UserState(Enum):
    DONE = 1
    WAITING_TO_RECEIVE_PDF_FILE = 2
