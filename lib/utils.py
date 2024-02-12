def utils():
    print("From Utils")

import time
import os
from rich import print as rprint

def please_wait(seconds=3):
    for _ in range(seconds):
        time.sleep(1)
        os.system("clear")
        rprint("[green]Please wait" + "." * (_ + 1))


# Move to utils folder
def exit_message():
    '''
    TBD
    '''
    rprint("[red]The program is now exiting")
    please_wait()
    rprint("Goodbye!")
    time.sleep(1)
    os.system("clear")

    raise SystemExit
