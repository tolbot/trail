#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   could probably work with Python2.x but never tested ...

"""Convenience wrapper, for running trail.py (package form), directly from source tree.

Example usage:

./trail-runner enter some text here ...      # Save new trail, in current directory
./trail-runner -g enter some text here ...   # Save new "global" trail, found in ~/.trail
./trail-runner                               # Print current directory trails
./trail-runner -g                            # Print "global" trails.
"""

from trail.trail import main

if __name__ == '__main__':
    main()
