#!/usr/bin/env python
"""
Usage:
    Amity create_room <roomtype> <roomname>
    Amity add_person <firstname> <lastname> <role> [<accomodation>]
    Amity reallocate_person <person_identifier> <new_room_name>
    Amity load_people
    Amity print_allocations [--o=<filename>]
    Amity print_unallocated [--o=<filename>]
    Amity print_room <room_name>
    Amity save_state [--db=sqlite_database]
    Amity load_state <sqlite_database>
    Amity (-i | --interactive)
    Amity (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    --o=<filename> specifies the file name
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
import os
import re

from docopt import docopt, DocoptExit
from colorama import *
from pyfiglet import figlet_format
from termcolor import colored, cprint
from models.amity import Amity



cprint(figlet_format("AMITY ROOM ALLOCATION".center(
    30), font="standard"), "blue", "on_yellow", attrs=["blink"])
cprint("\n")

def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print(colored('Invalid Command!', 'red'))
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn

    # def start():
    #     os.system("clear")
    #     print(__doc__)


class AmityApp (cmd.Cmd):
    #text = cprint('Amity Room Allocation', 'green', 'on_red')
    #text = colored('', 'red', attrs=['reverse', 'blink'])
    intro = 'Welcome to amity room allocations!' \
        + ' (type help for a list of commands.)'
    prompt = '(amity)'
    amity = Amity()

    @docopt_cmd
    def do_create_room(self, args):
        """Usage: create_room <roomtype> <roomname>..."""
        if not re.match("^[A-Za-z]*$", args['<roomtype>']):
            print(colored("Invalid input! Please enter roomtype in string format", "red"))
        elif not re.match("^[A-Za-z]*$", ''.join(args['<roomname>'])):
            print(colored("Invalid input! Please enter roomname in string format", "red"))
        else:
            print(self.amity.create_room(args['<roomtype>'], args['<roomname>']))


    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <firstname> <lastname> <role> [<accomodation>]"""
        if not re.match("^[A-Za-z]*$", args['<firstname>']):
            print(colored("Invalid input! Please enter firstname in string format", "red"))
        elif not re.match("^[A-Za-z]*$", args['<lastname>']):
            print(colored("Invalid input! Please enter lastname in string format", "red"))
        elif not re.match("^[A-Za-z]*$", args['<role>']):
            print(colored("Invalid input! Please enter role in string format", "red"))
        elif not re.match("^[A-Za-z]*$", args['<accomodation>']):
            print(colored("Invalid input! Please enter accomodation in string format", "red"))
        else:
            print(self.amity.add_person(args['<firstname>'], args['<lastname>'],
                                        args['<role>'], args['<accomodation>']))

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people [--o=<filename>]"""
        if not re.match("^[A-Za-z]*$", args['--o']):
            print(colored("Invalid input! Please enter filename in string format", "red"))
        else:
            print(self.amity.load_people(args['--o']))

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <roomname>"""
        if not re.match("^[A-Za-z]*$", args['<roomname>']):
            print(colored("Invalid input! Please enter room name in string format", "red"))
        else:
            print(self.amity.print_room(args['<roomname>']))

    @docopt_cmd
    def do_reallocate_person(self, args):
        """ Usage: reallocate_person <person_identifier> <new_room_name> """
        if not re.match("^[0-9]+$", args['<person_identifier>']):
            print(colored("Invalid input!"+
                          " Please enter person_identifier in ID number format", "red"))
        elif not re.match("^[A-Za-z]*$", args['<new_room_name>']):
            print(colored("Invalid input! Please enter the newroom name in string format", "red"))
        else:
            print(self.amity.reallocate_person(args
                                               ['<person_identifier>'], args['<new_room_name>']))


    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=<filename>]"""

        self.amity.print_allocations(args)

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--o=<filename>]"""
        self.amity.print_unallocated(args)

    @docopt_cmd
    def do_print_all_people(self, args):
        """Usage: print_all_people"""
        self.amity.print_all_people(args)

    @docopt_cmd
    def do_print_all_rooms(self, args):
        """Usage: print_all_rooms"""
        self.amity.print_all_rooms(args)

    @docopt_cmd
    def do_delete_person(self, args):
        """Usage: delete_person <personid>"""
        if not re.match("^[0-9]+$", args['<personid>']):
            print(colored("Invalid input!"+
                          " Please enter person_identifier in ID number format", "red"))
        else:
            print(self.amity.delete_person(args['<personid>']))

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""

        self.amity.save_state(args)

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <database>"""

        self.amity.load_state(args['<database>'])

    def do_quit(self, args):
        """Quits out of Interactive Mode."""

        print(colored('Adios! Hope to see you again soon', 'green'))
        exit()

#opt = docopt(__doc__, sys.argv[1:])

if __name__ == '__main__':
    print(colored(__doc__, 'green', 'on_blue', attrs=['bold']))
    AmityApp().cmdloop()
# if opt['--interactive']:
#     AmityApp().cmdloop()

# print(opt)