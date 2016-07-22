#!/usr/bin/python
#-*- coding: utf-8 -*-

from controlserver import control_main
from mission_control import ssh2
import sys
import os


if __name__=='__main__':

    if len(sys.argv) == 2:
        control_main(sys.argv[1])
    elif len(sys.argv) == 3 and 'ssh' == sys.argv[1]:
        ssh2(sys.argv[2])
    else:
        sys.exit(1)

