#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fixes import elementary_specific, general_fixes, device_specific_fixes

__author__ = 'Ian Richardson'

# You must run this file as superuser

import os
import platform


print("Script made by Ian Richardson / github.com/iantrich/, for public use")
print("I take no responsibility should anything go wrong while using this script.")
cont = raw_input("Use at your own risk. Do you wish to continue? [Y/n] ")
if cont is not 'y' and cont is not 'Y':
    exit()

raw_input("Please connect to internet service before continuing. Hit Enter when ready...")

print("1. Install software manually\n2. Install all default software (Guake, git, Numix themes, wingpanel, tlp, Chrome, gimp, LibreOffice, VLC, qBittorrent, glipper, Natural Scrolling (OS X Style), and Oracle JDK 7")
install_mode = raw_input("Choose your method: ")

print("What model do you have?\n1. C720\n2. HP 14\n3. Other")
hardware_model = raw_input("")

install_kernel = raw_input("Install Kernel 3.17? [Y/n] ")
if cont is not 'y' and cont is not 'Y':
    install_kernel.install_3_17()

distro_name, distro_version, distro_id = platform.linux_distribution() #Get Distroinformation

general_fixes.apply_general_fixes() #For all distros and versions

keys = raw_input("Remap Left, Right, Refresh, Display, Window, Search(Super_L) and Shift+Backspace(Delete) to function properly? The Search button will only be properly mapped on the HP 14. [Y/n]?")
if keys == "y" or keys == "Y":
    os.system("apt-get install -y xbindkeys xdotool")
    general_fixes.fix_mediakeys()

if hardware_model == "1": #C720 specific
    pass
elif hardware_model == "2": #HP14 specific
    if keys == "y" or keys == "Y":
        device_specific_fixes.map_superkey_hp14()

#Distro specific fixes
if distro_name == "Ubuntu":
    if distro_version == "12.04" or distro_version == "12.10":
        general_fixes.adjust_touchpad_sensitivity()
    elif distro_version == "14.04":
        general_fixes.install_chromeos_touchpad_drivers()
    elif distro_version == "14.04":
        #TODO coming version, may need additional fixes
        pass
elif distro_name == '"elementary OS"':
    elementary_specific.elementary_tweaks(distro_version)
    if distro_version == "0.2": #Luna
        general_fixes.adjust_touchpad_sensitivity()
        elementary_specific.wingpanel()
    elif distro_version == "0.3": #Freya
        general_fixes.install_chromeos_touchpad_drivers()
else:
    print "Your distribution is not supported. No specific fixes applied."

print("Installing any remaining dependencies")
os.system("apt-get install -f -y")

print("Checking for any updates")
os.system("apt-get upgrade -y")
os.system("apt-get dist-upgrade -y")

print("Removing leftovers")
os.system("apt-get autoremove -y")

# Restart the system
raw_input("Your system will now reboot so that all changes can take effect. Thanks for using my script and to all those who offered suggestions")
os.system("reboot")

