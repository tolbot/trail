#!/usr/bin/env python3

"""Keep track of your thoughts. Usage:

./trail.py enter some text here ...      # Save new trail, in current directory
./trail.py -g enter some text here ...   # Save new "global" trail, found in ~/.trail
./trail.py                               # Print current directory trails
./trail.py -g                            # Print "global" trails.
"""

import sys      # for proper exit.
import os       # for OS path checking.
import datetime
import calendar


py3 = sys.version_info[0] > 2  # creates boolean value for test that Python major version > 2
global_flag_used = False


class Trail(object):
    def __init__(self):
        self.created_timestamp = self._get_now_timestamp()  # eg: "Thu 25AUG17 04:16:53"
        self.content = "bla bla bla"

    @staticmethod
    def _get_now_timestamp():
        now_date = datetime.date.today()
        now_date_time = datetime.datetime.now()
        dayname = calendar.day_name[now_date.weekday()][:3]  # get 3 letter day name (of the week).
        created_timestamp = '{} {:02d}{}{} {:02d}:{:02d}:{:02d}'.format(dayname,
                                                                        now_date.day,
                                                                        calendar.month_name[now_date.month][:3].upper(),
                                                                        str(now_date.year)[2:],
                                                                        now_date_time.hour,
                                                                        now_date_time.minute,
                                                                        now_date_time.second)
        return created_timestamp

    def get_trail_string(self):
        return '{}  {}'.format(self.created_timestamp, self.content)


def print_args():
    print("Total arguments:")
    total = len(sys.argv)
    print(total)
    for lll in sys.argv:
        print(str(lll))


def get_trail_content_string_from_args():
    global global_flag_used
    # Check 1st arg if -g is used
    if sys.argv[1] == "-g":
        global_flag_used = True
        d = 2  # delta = 2, to skip the -g argument.
    else:
        global_flag_used = False
        d = 1
    return " ".join(sys.argv[d:])  # join args with single space.


def get_tags_from_user_input():
    #                                         TODO: sanitise input.
    q = "Enter tags (:separated): "
    if py3:
        return input(q)
    else:
        return raw_input(q)


def save_to_file(trail):
    global global_flag_used

    if global_flag_used:                    # TODO: these paths probaly won't work on windows.
        path_to_save = "{}/.trail/.trail".format(os.path.expanduser("~"))   # home dir.
    else:
        path_to_save = "./.trail"                                           # "current" dir.

    # If .trail doesn't exist, create it and insert header.
    if not os.path.isfile(path_to_save):
        if global_flag_used:
            tags_string = "global trails:"
        else:
            tags_string = get_tags_from_user_input()
        with open(path_to_save, "w") as f:          # TODO : try: ... except IOError: ...
            f.write("{}\n".format(tags_string))
        print("New .trail file created in {}/.trail".format(os.getcwd()))

    # append trail
    with open(path_to_save, "a") as f:
        f.write(trail.get_trail_string())
        f.write("\n")  # append newline at the end to avoid "partial lines" symbol in zsh;


def print_local_trail_file():
    with open('./.trail', 'r') as f:
        c = f.read()
    print(c)


def print_global_trail_file():
    with open("{}/.trail/.trail".format(os.path.expanduser("~")), 'r') as f:
        c = f.read()
    print(c)


def main():
    global global_flag_used

    if len(sys.argv) == 1:      # when excecuting just ./trail.py, with no args.
        print_local_trail_file()
        return

    # Check if -g is used.
    if len(sys.argv) > 1:
        if sys.argv[1] == "-g":
            global_flag_used = True

    # Check if ONLY -g is used.
    if global_flag_used and len(sys.argv) == 2:
        print_global_trail_file()
        return

    # Rest of use cases ...
    trail_content_string = get_trail_content_string_from_args()

    # Create a new trail
    trail = Trail()
    trail.content = trail_content_string

    save_to_file(trail)

    print(trail.get_trail_string())


if __name__ == '__main__':
    sys.exit(main())