import time
import os
from rich import print as rprint

def please_wait(seconds=3):
    for _ in range(seconds):
        time.sleep(1)
        os.system("clear")
        rprint("[green]Please wait" + "." * (_ + 1))