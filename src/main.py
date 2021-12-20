"""
A command-line tool example.

This file shows how you can let the user of a tool provide
data for your program. The arguments that a user provides
on the command-line can always be found in the list sys.argv.
The first item in this list is the name of the program, and
if there are any additional arguments they come after that.
So, you can test how many arguments you got by taking
len(sys.argv) and subtracting one for the name of the program,
and you can search through the sys.argv list for flags, or use
positional arguments by looking at the right indices.

We want the first argument, argv[1], to specify a sub-command. We
need to check that we have the at least one argument, and after
that, we can handle the appropriate one.

Both subcommands take the same arguments, so we can set those up before
we dispatch to the command, but this need not always be the case. When
not, you simply handle the remaining arguments in a command-specific
way, but you will do similar kinds of things as we do here.

The arguments for both sub-commands specify where we get the input
data from, and where we should write the output to, but we allow
defaults for both. If we have no file arguments, we will read
the input from stdin (available from sys.stdin) and we will write
the output to stdout (available from sys.stdout). If there is a single
file argument, it specifies the input file, so we will read from there
and print to stdout. If there are two file arguments, we have both
our input and output file. We can use len(sys.argv) to pick which case
we are in, remembering that the first element in sys.argv is the program
name and the second is the sub-command:

if len(sys.argv) == 2:
    # zero file arguments
elif len(sys.argv) == 3:
    # one file argument
elif len(sys.argv) == 4:
    # two file arguments
else:
    # more than two arguments; that is an error

or we can use the new pattern matching syntax from Python 3.10
and do this, 

match len(sys.argv):
    case 2:
        # zero file arguments
    case 3:
        # one file argument
    case 4:
        # two file arguments
    case _:
        # more than two arguments; that is an error

There is no difference between the two ways of doing it, so it
is entirely a question of taste.

The code below uses the second form to select the input and the
output file. The standard input file is found in sys.stdin and the
standard output file is found in sys.stdout. If we have a file name
we can open the file with open("filename") or open("filename", 'r')
if we want to read from it (for the input data) or with
open("filename", 'w') if we want to write to it (for the output data).

If we want to report erroneous situations, we should use sys.stderr. That way,
we do not mix error messages with the proper output that might go to sys.stdout.
If an error is so grievous that we need to inform the user about it more strongly,
we should report it as the exit status of the program. The exit status is something
the shell can check for, and the user can program around in shell-scripts. If a
program terminates normally, the exit status should be zero, and if something
went wrong, it should be non-zero. If you do nothing, Python will automatically
exit with a zero status, but you can use sys.exit(n) to exit with status n.

We are not checking if the files can be opened in this program, so errors there
are handled by Python (and it will set a proper exit status itself). We want
to report an error if we do not get the right number of arguments, though,
so there we write a message to stderr and exit with a non-zero status.

If we get past the argument parsing, the program runs the translations using
your functions. It does not check that the input is in a valid format, and
we do no error handling, but it is a beginning. We can learn how to do better
at a later time.

"""

import sys

import align
import cigar


def to_cig_cmd(infile, outfile) -> None:
    """Run the to_cig subcommand."""
    for line in infile:
        x = line.strip()
        y = next(infile).strip()
        _ = next(infile)
        cig = cigar.edits_to_cigar(align.edits(x, y))
        print(x.replace('-', ''),
              y.replace('-', ''),
              cig,
              sep='\t', file=outfile)


def from_cig_cmd(infile, outfile) -> None:
    """Run the from_cig subcommand."""
    for line in infile:
        # important to split on \t to handle empty strings
        x, y, cig = line.split('\t')
        x, y = align.align(x, y, cigar.cigar_to_edits(cig))
        print(x, file=outfile)
        print(y, file=outfile)
        print(file=outfile)


# You do not need to indent a command-line tool's code under
# a 'if __name__ == __main__:' construction, but it is common
# practise (if not exactly *best* practise). The idea behind
# it is this: when you import a Python file as a module, the
# __name__ variable is the name of the module, but if you run
# it as a program, __name__ will be '__main__'. So, this
# construction lets you specify code that should only be run
# when you use a file as a program, but not if you import
# the file for use as a module.
if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Missing subcommand argument.", file=sys.stderr)
        sys.exit(1)
    if sys.argv[1] not in ["to_cig", "from_cig"]:
        print(f"Unknown subcommand {sys.argv[1]}.", file=sys.stderr)
        sys.exit(1)

    # Checking arguments and getting the files
    infile, outfile = sys.stdin, sys.stdout
    match len(sys.argv):
        case 2:
            # zero file arguments
            pass
        case 3:
            # one file argument
            print("Feature not implemented.", file=sys.stderr)
            sys.exit(1)
        case 4:
            # two file arguments
            print("Feature not implemented.", file=sys.stderr)
            sys.exit(1)
        case _:
            # either too few or too many arguments
            print("Incorrect number of arguments.", file=sys.stderr)
            sys.exit(1)

    if sys.argv[1] == "to_cig":
        to_cig_cmd(infile, outfile)
    elif sys.argv[1] == "from_cig":
        from_cig_cmd(infile, outfile)
    else:
        # The check above should prevent this, but it is always good
        # to program defensively...
        print(f"Unknown command '{sys.argv[1]}'.", file=sys.stderr)
        sys.exit(1)

    # It is polite to close files when we no longer need them.
    # It doesn't matter here because we are just about to terminate
    # the entire program, but it is best to get into the habit
    # so we don't forget later, where it might matter more.
    infile.close()
    outfile.close()
