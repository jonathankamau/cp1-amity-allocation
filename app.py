#!/usr/bin/env python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.
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
from docopt import docopt, DocoptExit
from termcolor import colored, cprint
from models.amity import Amity


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

            print('Invalid Command!')
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
        print(self.amity.create_room(args['<roomtype>'], args['<roomname>']))


    @docopt_cmd
    def do_add_person(self, args):
        """Usage: add_person <firstname> <lastname> <role> [<accomodation>]"""
        print(self.amity.add_person(args['<firstname>'], args['<lastname>'],
                                    args['<role>'], args['<accomodation>']))

    @docopt_cmd
    def do_load_people(self, args):
        """Usage: load_people [--o=<filename>]"""

        print(self.amity.load_people(args['--o']))

    @docopt_cmd
    def do_print_room(self, args):
        """Usage: print_room <roomname>"""

        print(self.amity.print_room(args['<roomname>']))

    @docopt_cmd
    def do_reallocate_person(self, args):
        """ Usage: reallocate_person <firstname> <lastname> <new_room_name> """
        person_identifier = "{} {}".format(args['<firstname>'], args['<lastname>'])
        new_room = args['<new_room_name>']
        print(self.amity.reallocate_person(person_identifier, new_room))


    @docopt_cmd
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=<filename>]"""

        self.amity.print_allocations(args['--o'])

    @docopt_cmd
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--o=<filename>]"""

        self.amity.print_unallocated(args['--o'])

    @docopt_cmd
    def do_save_state(self, args):
        """Usage: save_state [--db=sqlite_database]"""

        self.amity.save_state(args['--db'])

    @docopt_cmd
    def do_load_state(self, args):
        """Usage: load_state <database>"""

        self.amity.load_state(args['<database>'])

    def do_quit(self, args):
        """Quits out of Interactive Mode."""

        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    AmityApp().cmdloop()

print(opt)