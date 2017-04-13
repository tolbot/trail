# -*- coding: utf-8 -*-

"""trail.trail: provides entry point main()."""


import sys      # for proper exit.
import os       # for OS path checking.
import datetime
import calendar

__version__ = "0.1.0"

py3 = sys.version_info[0] > 2  # creates boolean value for test that Python major version > 2
global_flag_used = False
trail_db_path_file = "{}/.trail/.traildb".format(os.path.expanduser("~"))   # home dir.


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


def trail_in_global_db(path_to_trail):
    global trail_db_path_file

    # Check global traildb
    try:
        with open(trail_db_path_file, "r") as f:
            content = f.readlines()
    except IOError:
        print("Error accessing global .traildb in {}, for reading.".format(trail_db_path_file))
        return False

    trailsdb = [x.strip() for x in content]  # list; remove \n at end of each line.
    if path_to_trail.strip() in trailsdb:
        return True
    else:
        return False


def write_trail_in_global_db(path_file_of_trail):
    global trail_db_path_file

    try:
        with open(trail_db_path_file, "a") as f:
            f.write(path_file_of_trail)
            f.write("\n")
    except IOError:
        print("Error accessing global .traildb in {}, for appending.".format(trail_db_path_file))
    else:
        print(".traildb in {}, updated with {}.".format(trail_db_path_file, path_file_of_trail))


def save_to_file(trail):
    global global_flag_used

    # Determine whether it's a local or global trail.
    if global_flag_used:                    # TODO: these paths probaly won't work on windows.
        # .trail FILE, NOT .traildb !
        path_file_to_save = "{}/.trail/.trail".format(os.path.expanduser("~"))  # home dir.
    else:
        # path_file_to_save = "./.trail"
        #   will expand ".", so we can use same string in the traildb.
        path_file_to_save = "{}/.trail".format(os.getcwd())                     # "current" dir.

    # If .trail doesn't exist, create it and insert header.
    if not os.path.isfile(path_file_to_save):
        if global_flag_used:
            tags_string = "global trails:"
        else:
            tags_string = get_tags_from_user_input()
        try:
            with open(path_file_to_save, "w") as f:
                f.write("{}\n".format(tags_string))
        except IOError:
            print("Cannot write .trail file {}, (make sure you are not in \"home\" dir).".format(path_file_to_save))
            #   Usually, you cannot have dir+file with SAME name, under same (home) dir!
            return
            # TODO : handle above case better.
        else:
            print("New .trail file created, {}.".format(path_file_to_save))

    # Append trail.
    try:
        with open(path_file_to_save, "a") as f:
            f.write(trail.get_trail_string())
            f.write("\n")  # append newline at the end to avoid "partial lines" symbol in zsh;
    except IOError:
        print("Cannot access {}, to append trail.".format(path_file_to_save))
    # print trail, if success.
    print(trail.get_trail_string())

    # If needed, write to global traildb.
    if not trail_in_global_db(path_file_to_save):
        write_trail_in_global_db(path_file_to_save)


def print_global_trail_file():
    global_trail_path_file = "{}/.trail/.trail".format(os.path.expanduser("~"))
    try:
        with open(global_trail_path_file, 'r') as f:
            content = f.read()
    except IOError:
        content = "{} not found.".format(global_trail_path_file)
    print(content)


def print_local_trail_file():
    try:
        with open('./.trail', 'r') as f:
            content = f.read()
    except IOError:
        print(".trail not found. - Displaying global .trail instead:")
        print_global_trail_file()
        return
    else:
        print(content)


def main():
    global global_flag_used

    if len(sys.argv) == 1:      # when excecuting just ./__init__.py, with no args.
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
