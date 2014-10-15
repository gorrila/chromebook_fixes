#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ian Richardson'

# You must run this file as superuser

import urllib
import os
import fileinput
import sys
import platform
import subprocess

def checkFiles(username):
    files = {'kernel':False, 'suspend':False, 'files':False, 'grub':False, 'touchpad':False, 'xmodmap':False, 'xdotool':False}

    # Check if kernel is up to date
    if '3.17.0-031700-generic' in subprocess.Popen(["uname", "-r"], stdout=subprocess.PIPE).communicate()[0]:
        files.update({'kernel':True})

    try:
        if """#!/bin/sh
    # File: "/etc/pm/sleep.d/05_Sound".
    case "${1}" in
    hibernate|suspend)
    # Unbind ehci for preventing error
    echo -n "0000:00:1d.0" | tee /sys/bus/pci/drivers/ehci-pci/unbind
    # Unbind snd_hda_intel for sound
    echo -n "0000:00:1b.0" | tee /sys/bus/pci/drivers/snd_hda_intel/unbind
    echo -n "0000:00:03.0" | tee /sys/bus/pci/drivers/snd_hda_intel/unbind
    ;;
    resume|thaw)
    # Bind ehci for preventing error
    echo -n "0000:00:1d.0" | tee /sys/bus/pci/drivers/ehci-pci/bind
    # Bind snd_hda_intel for sound
    echo -n "0000:00:1b.0" | tee /sys/bus/pci/drivers/snd_hda_intel/bind
    echo -n "0000:00:03.0" | tee /sys/bus/pci/drivers/snd_hda_intel/bind
    ;;
    esac""" in open("/etc/pm/sleep.d/05_Sound").read():
            files.update({'suspend':True})

        if """echo EHCI > /proc/acpi/wakeup
    echo HDEF > /proc/acpi/wakeup
    echo XHCI > /proc/acpi/wakeup
    echo LID0 > /proc/acpi/wakeup
    echo TPAD > /proc/acpi/wakeup
    echo TSCR > /proc/acpi/wakeup
    echo 300 > /sys/class/backlight/intel_backlight/brightness
    rfkill block bluetooth
    /etc/init.d/bluetooth stop""" in open("/etc/rc.local").read():
            files.update({'rc':True})
    except IOError:
        print("05_Sound not yet created")

    if """GRUB_CMDLINE_LINUX_DEFAULT="quiet splash add_efi_memmap boot=local noresume noswap i915.modeset=1 tpm_tis.force=1 tpm_tis.interrupts=0 nmi_watchdog=panic,lapic\"""" not in open("/etc/default/grub").read():
        files.update({'grub':True})

    if "FingerLow" "5" in open("/usr/share/X11/xorg.conf.d/50-synaptics.conf").read():
        files.update({'touchpad':True})

    try:
        if """#!/bin/bash
    xmodmap -e "keycode 225 = Super_L";
    xmodmap -e “add mod4 = Super_L”;""" in open("/home/" + username + "/.xmodmap").read():
            files.update({'xmodmap':True})
    except IOError:
        print("xmodmap not yet created")
    try:
        if """"xdotool keyup F1; xdotool key alt+Left"
    F1
    "xdotool keyup F2; xdotool key alt+Right"
    F2
    "xdotool keyup F5; xdotool key super+a"
    F5
    "xdotool keyup F3; xdotool key ctrl+r"
    F3
    "xdotool keyup F4; xdotool key F11"
    F4
    "xdotool keyup shift+BackSpace; xdotool key Delete; xdotool keydown shift"
    shift+BackSpace
    "xdotool keyup F6; xdotool key XF86MonBrightnessDown"
    F6
    "xdotool keyup F7; xdotool key XF86MonBrightnessUp"
    F7
    "xdotool keyup F8; xdotool key XF86AudioMute"
    F8
    "xdotool keyup F9; xdotool key XF86AudioLowerVolume"
    F9
    "xdotool keyup F10; xdotool key XF86AudioRaiseVolume"
    F10""" in open("/home/" + username + "/.xbindkeysrc").read():
            files.update({'xdotool':True})
    except IOError:
        print("xbindkeysrc not yet created")

    return files;

def checkRepos():
    repos = subprocess.Popen(["find /etc/apt/", "-name *.list | xargs cat | grep  ^[[:space:]]*deb"], stdout=subprocess.PIPE).communicate()
    installedRepos = {};

    return installedRepos;


print("Script made by Ian Richardson / github.com/iantrich/, for public use")
print("I take no responsibility should anything go wrong while using this script.")
cont = raw_input("Use at your own risk. Do you wish to continue? [Y/n] ")
if cont is not 'y' and cont is not 'Y':
    exit()

raw_input("Please connect to internet service before continuing. Hit Enter when ready...")

if 'Luna' in open("/etc/os-release").read():
    version = 1
elif 'Freya' in open("/etc/os-release").read():
    version = 'freya'
elif 'Freya' in open("/etc/os-release").read():
    version = '12.04'
elif 'Freya' in open("/etc/os-release").read():
    version = '14.04'
else:
    version = 'other'

print("1. Install software manually\n2. Install all default software (Guake, git, Numix themes, wingpanel, tlp, Chrome, gimp, LibreOffice, VLC, qBittorrent, glipper, Natural Scrolling (OS X Style), and Oracle JDK 7")
manual = raw_input("Choose your method: ")

username = raw_input("Carefully enter your username: ")

print("What model do you have?\n1. C720\n2. HP 14\n3. Other")
model = raw_input("")

if manual is '1':
    if version is 'freya' or version is '12.04':
        driver = raw_input("Install ChromeOS touchpad driver? [Y/n]? ")
    guake = raw_input("Install Guake: A dropdown terminal? [Y/n]? ")
    git = raw_input("Install git? [Y/n] ")
    numix = raw_input("Install the beautiful numix theme and elementary tweaks? [Y/n]? ")
    if version is 'luna':
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

print("Check current kernel version")
if not files.get('kernel'):
    print("Grabbing kernel 3.17 stable...may take a few moments")
    kernel = urllib.URLopener()
    # Check if system is 32 or 64-bit
    if platform.architecture()[0] is "64bit":
        kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb", "/home/" + username + "/Downloads/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb")
        kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb", "/home/" + username + "/Downloads/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb")
    else:
        kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_i386.deb", "/home/" + username + "/Downloads/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_i386.deb")
        kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_i386.deb", "/home/" + username + "/Downloads/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_i386.deb")
    kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700_3.17.0-031700.201410060605_all.deb", "/home/" + username + "/Downloads/linux-headers-3.17.0-031700_3.17.0-031700.201410060605_all.deb")

    print("Remove old kernel")
    os.system("""apt-get remove --purge $(dpkg -l 'linux-image-*' | sed '/^ii/!d;/'"$(uname -r | sed "s/\(.*\)-\([^0-9]\+\)/\1/")"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d')""")

    print("Extract packages to update the kernel")
    os.system("dpkg -i ~/Downloads/*.deb")
    os.system("rm ~/Downloads/*.deb")

if not files.get('suspend'):
    print("Fix suspend and boot times")
    sound = open("/etc/pm/sleep.d/05_Sound", "w")
    sound.write("""#!/bin/sh
    # File: "/etc/pm/sleep.d/05_Sound".
    case "${1}" in
    hibernate|suspend)
    # Unbind ehci for preventing error
    echo -n "0000:00:1d.0" | tee /sys/bus/pci/drivers/ehci-pci/unbind
    # Unbind snd_hda_intel for sound
    echo -n "0000:00:1b.0" | tee /sys/bus/pci/drivers/snd_hda_intel/unbind
    echo -n "0000:00:03.0" | tee /sys/bus/pci/drivers/snd_hda_intel/unbind
    ;;
    resume|thaw)
    # Bind ehci for preventing error
    echo -n "0000:00:1d.0" | tee /sys/bus/pci/drivers/ehci-pci/bind
    # Bind snd_hda_intel for sound
    echo -n "0000:00:1b.0" | tee /sys/bus/pci/drivers/snd_hda_intel/bind
    echo -n "0000:00:03.0" | tee /sys/bus/pci/drivers/snd_hda_intel/bind
    ;;
    esac""")
    sound.close()
os.system("chmod +x /etc/pm/sleep.d/05_Sound")

if not files.get('rc'):
    # Edit rc.local
    for line in fileinput.input("/etc/rc.local", inplace=True):
        if "By default" not in line:
            sys.stdout.write(line)
        else:
            sys.stdout.write("""echo EHCI > /proc/acpi/wakeup
    echo HDEF > /proc/acpi/wakeup
    echo XHCI > /proc/acpi/wakeup
    echo LID0 > /proc/acpi/wakeup
    echo TPAD > /proc/acpi/wakeup
    echo TSCR > /proc/acpi/wakeup
    echo 300 > /sys/class/backlight/intel_backlight/brightness
    rfkill block bluetooth
    /etc/init.d/bluetooth stop""")

if not files.get('grub'):
    # Edit grub and update
    for line in fileinput.input("/etc/default/grub", inplace=True):
        if "GRUB_CMDLINE_LINUX_DEFAULT" not in line:
            sys.stdout.write(line)
        else:
            sys.stdout.write("""GRUB_CMDLINE_LINUX_DEFAULT="quiet splash add_efi_memmap boot=local noresume noswap i915.modeset=1 tpm_tis.force=1 tpm_tis.interrupts=0 nmi_watchdog=panic,lapic\"""")
    os.system("update-grub")
    os.system("update-grub2")

if version is 'luna' or '12.04':
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

if version is 'luna':
    if numix is 'y' or numix is 'Y':
        os.system("add-apt-repository -y ppa:numix/ppa")
        os.system("add-apt-repository -y ppa:versable/elementary-update")
        os.system("apt-get update -y")
        os.system("apt-get install -y numix-gtk-theme numix-icon-theme-circle elementary-tweaks")

    if wing is 'y' or wing is 'Y':
        if numix is not 'y' and numix is not 'Y':
            os.system("add-apt-repository ppa:numix/ppa")
            os.system("add-apt-repository ppa:versable/elementary-update")
            os.system("apt-get update")
    os.system("apt-get install wingpanel-slim super-wingpanel")

if version is 'freya' or '14.04':
    if driver is 'y' or driver is 'Y':
        if not subprocess.Popen(["[ -f /usr/share/X11/xorg.conf.d/50-touchpad-cmt-peppy.conf]", ""], stdout=subprocess.PIPE).communicate()[0]:
            os.system("add-apt-repository -y ppa:hugegreenbug/cmt")
            os.system("apt-get update -y")
            os.system("apt-get install -y libevdevc libgestures  xf86-input-cmt")
            os.system("mv /usr/share/X11/xorg.conf.d/50-synaptics.conf /usr/share/X11/xorg.conf.d/50-synaptics.conf.old")
            os.system("cp /usr/share/xf86-input-cmt/50-touchpad-cmt-peppy.conf /usr/share/X11/xorg.conf.d/")
    else:
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

    if numix is 'y' or numix is 'Y':
        os.system("add-apt-repository -y ppa:numix/ppa")
        os.system("add-apt-repository -y ppa:mpstark/elementary-tweaks-daily")
        os.system("apt-get update -y")
        os.system("apt-get install -y numix-gtk-theme numix-icon-theme-circle elementary-tweaks")

if guake is 'y' or guake is 'Y':
    os.system("apt-get install -y guake")
    os.system("ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/")

if git is 'y' or git is 'Y':
    os.system("apt-get install -y git")

if keys is 'y' or keys is 'Y':
    if not files.get('xmodmap'):
        os.system("apt-get install -y xbindkeys xdotool")
        # Map Super_L to the Search key
        # Create .xmodmap
        if model is "2":
            map = open("/home/" + username + "/.xmodmap", "w")
            map.write("""#!/bin/bash
    xmodmap -e "keycode 225 = Super_L";
    xmodmap -e “add mod4 = Super_L”;""")
            map.close()
            os.system("chmod +x ~/.xmodmap")
            os.system("ln -s ~/.xmodmap /etc/xdg/autostart/")

    # Remap all remaining top row keys and Delete to Shift+Backspace
    # Create .xbindkeysrc
    if not files.get("xdotool"):
        xbind = open("/home/" + username + "/.xbindkeysrc", "w")
        xbind.write(""""xdotool keyup F1; xdotool key alt+Left"
    F1
    "xdotool keyup F2; xdotool key alt+Right"
    F2
    "xdotool keyup F5; xdotool key super+a"
    F5
    "xdotool keyup F3; xdotool key ctrl+r"
    F3
    "xdotool keyup F4; xdotool key F11"
    F4
    "xdotool keyup shift+BackSpace; xdotool key Delete; xdotool keydown shift"
    shift+BackSpace
    "xdotool keyup F6; xdotool key XF86MonBrightnessDown"
    F6
    "xdotool keyup F7; xdotool key XF86MonBrightnessUp"
    F7
    "xdotool keyup F8; xdotool key XF86AudioMute"
    F8
    "xdotool keyup F9; xdotool key XF86AudioLowerVolume"
    F9
    "xdotool keyup F10; xdotool key XF86AudioRaiseVolume"
    F10""")
        os.system("chmod +x ~/.xbindkeysrc")

    #Set Fullscreen toggle to be F4
    os.system("""gsettings set org.gnome.desktop.wm.keybindings toggle-fullscreen "['F4']\"""")

if openJ is 'y' or openJ is 'Y':
    os.system("apt-get install -y openjdk-7-jdk")

if battery is 'y' or battery is 'Y':
    os.system("add-apt-repository -y ppa:linrunner/tlp")
    os.system("apt-get update -y")
    os.system("apt-get install -y tlp tlp-rdw")

if chrome is 'y' or chrome is 'Y':
    print("Downloading Chrome. This may take a few moments...")
    if platform.architecture()[0] is "64bit":
        kernel.retrieve("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", "/home/" + username + "/Downloads/google-chrome-stable_current_amd64.deb")
    else:
        kernel.retrieve("https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb", "/home/" + username + "/Downloads/google-chrome-stable_current_i386.deb")
    os.system("dpkg -i ~/Downloads/*.deb")
    os.system("rm ~/Downloads/*.deb")
    os.system("mv /usr/share/applications/google-chrome.desktop /usr/share/applications/google-chrome-stable.desktop")

if gimp is 'y' or gimp is 'Y':
    os.system("apt-get install -y gimp")

if libre is 'y' or libre is 'Y':
    os.system("apt-get install -y libreoffice")

if vlc is 'y' or vlc is 'Y':
    os.system("apt-get install -y vlc")

if bit is 'y' or bit is 'Y':
    os.system("apt-get install -y qbittorrent")

if glipper is 'y' or glipper is 'Y':
    os.system("apt-get install -y glipper")

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

