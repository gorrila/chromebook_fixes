#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'sinan.boecker'

import os
import getpass

def map_superkey_hp14(username):
    keymap = open("/home/" + username + "/.xmodmap", "w")
    keymap.write("""#!/bin/bash
        xmodmap -e "keycode 225 = Super_L";
        xmodmap -e “add mod4 = Super_L”;""")
    keymap.close()
    os.system("chmod +x ~/.xmodmap")
    os.system("ln -s ~/.xmodmap /etc/xdg/autostart/")
