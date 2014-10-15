#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fixes import elementary_fixes, general_fixes

__author__ = 'Ian Richardson'

# You must run this file as superuser

import urllib
import os
import fileinput
import sys
import platform
import subprocess
import fixes

def checkFiles(username):
    files = {'kernel':False, 'suspend':False, 'files':False, 'grub':False, 'touchpad':False, 'xmodmap':False, 'xdotool':False}

    # Check if kernel is up to date
    if '3.17.0-031700-generic' in subprocess.Popen(["uname", "-r"], stdout=subprocess.PIPE).communicate()[0]:
        files.update({'kernel':True})
    #
    # try:
    #     if """#!/bin/sh
    # # File: "/etc/pm/sleep.d/05_Sound".
    # case "${1}" in
    # hibernate|suspend)
    # # Unbind ehci for preventing error
    # echo -n "0000:00:1d.0" | tee /sys/bus/pci/drivers/ehci-pci/unbind
    # # Unbind snd_hda_intel for sound
    # echo -n "0000:00:1b.0" | tee /sys/bus/pci/drivers/snd_hda_intel/unbind
    # echo -n "0000:00:03.0" | tee /sys/bus/pci/drivers/snd_hda_intel/unbind
    # ;;
    # resume|thaw)
    # # Bind ehci for preventing error
    # echo -n "0000:00:1d.0" | tee /sys/bus/pci/drivers/ehci-pci/bind
    # # Bind snd_hda_intel for sound
    # echo -n "0000:00:1b.0" | tee /sys/bus/pci/drivers/snd_hda_intel/bind
    # echo -n "0000:00:03.0" | tee /sys/bus/pci/drivers/snd_hda_intel/bind
    # ;;
    # esac""" in open("/etc/pm/sleep.d/05_Sound", "r"):
    #         files.update({'suspend':True})
    #
    #     if """echo EHCI > /proc/acpi/wakeup
    # echo HDEF > /proc/acpi/wakeup
    # echo XHCI > /proc/acpi/wakeup
    # echo LID0 > /proc/acpi/wakeup
    # echo TPAD > /proc/acpi/wakeup
    # echo TSCR > /proc/acpi/wakeup
    # echo 300 > /sys/class/backlight/intel_backlight/brightness
    # rfkill block bluetooth
    # /etc/init.d/bluetooth stop""" in open("/etc/rc.local", "r"):
    #         files.update({'rc':True})
    # except IOError:
    #     print("05_Sound not yet created")
    #
    # if """GRUB_CMDLINE_LINUX_DEFAULT="quiet splash add_efi_memmap boot=local noresume noswap i915.modeset=1 tpm_tis.force=1 tpm_tis.interrupts=0 nmi_watchdog=panic,lapic\"""" not in open("/etc/default/grub").read():
    #     files.update({'grub':True})
    #
    # if "FingerLow" "5" in open("/usr/share/X11/xorg.conf.d/50-synaptics.conf", "r"):
    #     files.update({'touchpad':True})
    #
    # try:
    #     if """#!/bin/bash
    # xmodmap -e "keycode 225 = Super_L";
    # xmodmap -e “add mod4 = Super_L”;""" in open("/home/" + username + "/.xmodmap", "r"):
    #         files.update({'xmodmap':True})
    # except IOError:
    #     print("xmodmap not yet created")
    # try:
    #     if """"xdotool keyup F1; xdotool key alt+Left"
    # F1
    # "xdotool keyup F2; xdotool key alt+Right"
    # F2
    # "xdotool keyup F5; xdotool key super+a"
    # F5
    # "xdotool keyup F3; xdotool key ctrl+r"
    # F3
    # "xdotool keyup F4; xdotool key F11"
    # F4
    # "xdotool keyup shift+BackSpace; xdotool key Delete; xdotool keydown shift"
    # shift+BackSpace
    # "xdotool keyup F6; xdotool key XF86MonBrightnessDown"
    # F6
    # "xdotool keyup F7; xdotool key XF86MonBrightnessUp"
    # F7
    # "xdotool keyup F8; xdotool key XF86AudioMute"
    # F8
    # "xdotool keyup F9; xdotool key XF86AudioLowerVolume"
    # F9
    # "xdotool keyup F10; xdotool key XF86AudioRaiseVolume"
    # F10""" in open("/home/" + username + "/.xbindkeysrc", "r"):
    #         files.update({'xdotool':True})
    # except IOError:
    #     print("xbindkeysrc not yet created")

    return files;

def checkRepos():
    # repos = subprocess.Popen(["find /etc/apt/", "-name *.list | xargs cat | grep  ^[[:space:]]*deb"], stdout=subprocess.PIPE).communicate()
    installedRepos = {};

    return installedRepos;


print("Script made by Ian Richardson / github.com/iantrich/, for public use")
print("I take no responsibility should anything go wrong while using this script.")
cont = raw_input("Use at your own risk. Do you wish to continue? [Y/n] ")
if cont is not 'y' and cont is not 'Y':
    exit()

raw_input("Please connect to internet service before continuing. Hit Enter when ready...")

print("1. Install software manually\n2. Install all default software (Guake, git, Numix themes, wingpanel, tlp, Chrome, gimp, LibreOffice, VLC, qBittorrent, glipper, Natural Scrolling (OS X Style), and Oracle JDK 7")
install_mode = raw_input("Choose your method: ")

username = raw_input("Carefully enter your username: ")

print("What model do you have?\n1. C720\n2. HP 14\n3. Other")
hardware_model = raw_input("")

distro_name, distro_version, distro_id = platform.linux_distribution()
if "ubuntu" in distro_name:
    //ubuntu fixes
    general_fixes()
elif "elementary" in distro_name:
    //elementary_fixes
else:
    print "Your distribution is not supported. Resume?"








if install_mode is '1':
    if distro is 'freya' or distro is '14.04':
        driver = raw_input("Install ChromeOS touchpad driver? [Y/n]? ")
    guake = raw_input("Install Guake: A dropdown terminal? [Y/n]? ")
    git = raw_input("Install git? [Y/n] ")
    numix = raw_input("Install the beautiful numix theme and elementary tweaks? [Y/n]? ")
    if distro is 'luna':
        wing = raw_input("Install slim and super wingpanel? If you don't know what they are look it up. [Y/n} ")
    keys = raw_input("Remap Left, Right, Refresh, Display, Window, Search(Super_L) and Shift+Backspace(Delete) to function properly? The Search button will only be properly mapped on the HP 14. [Y/n]? ")
    battery = raw_input("Install TLP Battery Saver? [Y/n]? ")
    chrome = raw_input("Install Chrome browser? [Y/n]? ")
    gimp = raw_input("Install GIMP image editor? [Y/n]? ")
    libre = raw_input("Install LibreOffice Suite? [Y/n]? ")
    vlc = raw_input("Install VLC media player? [Y/n]? ")
    bit = raw_input("Install qBittorrent? [Y/n]? ")
    glipper = raw_input("Install glipper clibboard manager? [Y/n]? ")
    scroll = raw_input("Install OS X style natural scrolling? [Y/n]? ")
    java = raw_input("Install Oracle Java 7? [Y/n]? ")
    if java is not 'y' and java is not 'Y':
        openJ = raw_input("Install Open JDK 7? [Y/n]? ")
else:
    guake = git = numix = driver = wing = keys = battery = chrome = gimp = libre = vlc = bit = glipper = scroll = java = 'y'

files = checkFiles(username)

repos = checkRepos()

if java is 'y' or java is 'Y':
        raw_input("Follow the on-screen instructions to finish the Java installation. It might take awhile, but this is the last prompt from me")
        os.system("add-apt-repository -y ppa:webupd8team/java")
        os.system("apt-get update -y")
        os.system("apt-get install -y python-software-properties oracle-java7-installer")


if distro is 'luna' or '12.04':
    if not files.get('touchpad'):
        # Adjust touchpad sensitivity
        print("Adjusting touchpad to be more sensitive as ChromeOS touchpad driver had not been backported to 12.04 yet")
        section = False
        for line in fileinput.input("/usr/share/X11/xorg.conf.d/50-synaptics.conf", inplace=True):
            if section:
                sys.stdout.write("""      Option "FingerLow" "5"
              Option "FingerHigh" "16\"\n""")
                section = False
            if "input/event*" not in line:
                sys.stdout.write(line)
            else:
                sys.stdout.write(line)
                section = True

    print("Upgrade Xserver for better performance")
    os.system("apt-get install -y xserver-xorg-lts-trusty")







if battery is 'y' or battery is 'Y':
    os.system("add-apt-repository -y ppa:linrunner/tlp")
    os.system("apt-get update -y")
    os.system("apt-get install -y tlp tlp-rdw")


if scroll is 'y' or scroll is 'Y':
    os.system("add-apt-repository -y ppa:zedtux/naturalscrolling")
    os.system("apt-get update -y")
    os.system("apt-get install -y naturalscrolling")
    os.system(" ln -s /usr/share/applications/naturalscrolling.desktop /etc/xdg/autostart/")

print("Installing any remaining dependencies")
os.system("apt-get install -f -y")

print("Checking for any updates")
os.system("apt-get upgrade -y")
os.system("apt-get dist-upgrade -y")

print("Removing leftovers")
os.system("apt-get autoremove -y")

# if version is 'luna' or '12.04':
#     # Create script to double check the touchpad config file
#     auto = open("/home/" + username + "/Downloads/auto.py", "w")
#     auto.write("""#!/usr/bin/env python
#     # -*- coding: utf-8 -*-
#     __author__ = 'Ian Richardson'
#
#     import fileinput
#     import sys
#
#     section = False
#     edited = False
#
#     for line in fileinput.input("/usr/share/X11/xorg.conf.d/50-synaptics.conf", inplace=True):
#         if "FingerHigh" in line:
#             edited = True
#
#         sys.stdout.write(line)
#
#     if not edited:
#         for line in fileinput.input("/usr/share/X11/xorg.conf.d/50-synaptics.conf", inplace=True):
#             if section:
#                 sys.stdout.write(\"""      Option "FingerLow" "5"
#             Option "FingerHigh" "16"\\n""\")
#                 section = False
#             if "input/event*" not in line:
#                 sys.stdout.write(line)
#             else:
#                 sys.stdout.write(line)
#                 section = True""")
#     os.system("chmod +x /home/" + username + "/Downloads/auto.py")
#
#     # Create bash script that calls the python script with admin rights and deletes all scripts once complete
#     bash = open("/etc/init.d/auto", "w")
#     bash.write("""#! /bin/bash
#     sudo python /home/""" + username + """/Downloads/auto.py
#     sudo rm /home/""" + username + """/Downloads/auto.py
#     sudo rm /home/""" + username + """/Downloads/elementary12.py
#     sudo rm -- "$0"
#     sudo rm /etc/rc2.d/S99myscript
#     """)
#     os.system("chmod +x /etc/init.d/auto")
#     os.system("ln -s /etc/init.d/auto /etc/rc2.d/S99myscript")

# Restart the system
raw_input("Your system will now reboot so that all changes can take effect. Thanks for using my script and to all those who offered suggestions")
os.system("reboot")

