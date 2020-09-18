
import asyncio
import random
import time as t
from tkinter import *
from tkinter import messagebox
import asyncio
import threading
import random

def _asyncio_thread(async_loop):
    async_loop.run_until_complete(do_urls())


def do_tasks(async_loop):
    """ Button-Event-Handler starting the asyncio part. """
    do_freezed()
    threading.Thread(target=_asyncio_thread, args=(async_loop,)).start()


async def one_url(url):
    """ One task. """
    sec = random.randint(1, 8)
    await asyncio.sleep(sec)
    return 'url: {}\tsec: {}'.format(url, sec)

async def do_urls():
    """ Creating and starting 10 tasks. """
    tasks = [one_url(url) for url in range(10)]
    completed, pending = await asyncio.wait(tasks)
    results = [task.result() for task in completed]
    print('\n'.join(results))


def do_freezed():
    messagebox.showinfo(message='Tkinter is reacting.')

def main(async_loop):
    root = Tk()
    Button(master=root, text='Asyncio Tasks', command= lambda:do_tasks(async_loop)).pack()
    root.mainloop()

if __name__ == '__main__':
    async_loop = asyncio.get_event_loop()
    main(async_loop)
"""


  




shot: 1.5

small:3
medium: 5
large: 7


Display Drinks Percentage Math
medium * ratio = OZ
example:
    5 * .24 = 


MATH for converting drink size and ratio to actual liquor dispensed
90
150
210


150 * .11 = 16.5 / 10 = 1.65 seconds
150 Militiers 
.11 is recipe ratio
10 = rate of which pumps can flow (example 10 militers per second)



90* .10 = 9 / 10 = .9 seconds
90 militiers (cup size)
.10 = recipe ratio
10 = rate of which pumps can flow (example 10 militers per second)

90 * .02 = 1.8 /10 = .18 seconds
90 militers (cup size)
.02 =  recipe ratio
10 = rate of which pumps can flow (Example 10 militers per seoncd)




LEAST PRIORITY:
_________________________________________________________________________
TO DISPLAY STONGER MENU

if ingrediants <=4 && ingrediants == only one alcohol:
    display stronger menu:

    if ingrediants == dict[Vodka, Tequila, Rum, Whisky, Gin]




"""