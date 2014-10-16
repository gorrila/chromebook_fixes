#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ian Richardson'

# You must run this file as superuser

import urllib
import os
import fileinput
import sys
import platform

print("Script made by Ian Richardson / iantrich.com, for public use")
print("I take no responsibility should anything go wrong while using this script.")
cont = raw_input("Use at your own risk. Do you wish to continue? [Y/n] ")
if cont != 'y' and cont != 'Y':
    exit()

raw_input("Please connect to internet service before continuing. Hit Enter when ready...")

print("1. elementary OS Luna\n2. elementary OS Freya")
version = raw_input("Choose your version: ")

print("1. Install software manually\n2. Install all default software (Guake, git, Numix themes, wingpanel, tlp, Chrome, gimp, LibreOffice, VLC, qBittorrent, glipper, Natural Scrolling (OS X Style), and Oracle JDK 7")
manual = raw_input("Choose your method: ")

username = raw_input("Carefully enter your username: ")

print("What model do you have?\n1. C720\n2. HP 14\n3. Other")
model = raw_input("")

if manual == '1':
    if version == '2':
        driver = raw_input("Install ChromeOS touchpad driver? [Y/n]? ")
    guake = raw_input("Install Guake: A dropdown terminal? [Y/n]? ")
    git = raw_input("Install git? [Y/n] ")
    numix = raw_input("Install the beautiful numix theme and elementary tweaks? [Y/n]? ")
    if version == '1':
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
    if java != 'y' and java != 'Y':
        openJ = raw_input("Install Open JDK 7? [Y/n]? ")
else:
    guake = git = numix = driver = wing = keys = battery = chrome = gimp = libre = vlc = bit = glipper = scroll = java = 'y'
    openJ = 'n'
if java == 'y' or java == 'Y':
        raw_input("Follow the on-screen instructions to finish the Java installation. It might take awhile, but this is the last prompt from me")
        os.system("add-apt-repository -y ppa:webupd8team/java")
        os.system("apt-get update -y")
        os.system("apt-get install -y python-software-properties oracle-java7-installer")

print("Grabbing kernel 3.17 stable...may take a few moments")
kernel = urllib.URLopener()
# Check if system is 32 or 64-bit
if platform.architecture()[0] == "64bit":
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

# Edit grub and update
for line in fileinput.input("/etc/default/grub", inplace=True):
    if "GRUB_CMDLINE_LINUX_DEFAULT" not in line:
        sys.stdout.write(line)
    else:
        sys.stdout.write("""GRUB_CMDLINE_LINUX_DEFAULT="quiet splash add_efi_memmap boot=local noresume noswap i915.modeset=1 tpm_tis.force=1 tpm_tis.interrupts=0 nmi_watchdog=panic,lapic\"""")
os.system("update-grub")
os.system("update-grub2")

if version == '1':
    # Upgrade Xserver for better performance
    os.system("apt-get install -y xserver-xorg-lts-trusty")

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

    if numix == 'y' or numix == 'Y':
        os.system("add-apt-repository -y ppa:numix/ppa")
        os.system("add-apt-repository -y ppa:versable/elementary-update")
        os.system("apt-get update -y")
        os.system("apt-get install -y numix-gtk-theme numix-icon-theme-circle elementary-tweaks")

    if wing == 'y' or wing == 'Y':
        if numix != 'y' and numix != 'Y':
            os.system("add-apt-repository ppa:numix/ppa")
            os.system("add-apt-repository ppa:versable/elementary-update")
            os.system("apt-get update")
    os.system("apt-get install wingpanel-slim super-wingpanel")

if version == '2':
    if driver == 'y' or driver == 'Y':
        os.system("add-apt-repository -y ppa:hugegreenbug/cmt")
        os.system("apt-get update -y")
        os.system("apt-get install -y libevdevc libgestures  xf86-input-cmt")
        os.system("mv /usr/share/X11/xorg.conf.d/50-synaptics.conf /usr/share/X11/xorg.conf.d/50-synaptics.conf.old")
        os.system("cp /usr/share/xf86-input-cmt/50-touchpad-cmt-peppy.conf /usr/share/X11/xorg.conf.d/")

if guake == 'y' or guake == 'Y':
    os.system("apt-get install -y guake")
    os.system("ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/")

if git == 'y' or git == 'Y':
    os.system("apt-get install -y git")

if numix == 'y' or numix == 'Y' and version == '2':
    os.system("add-apt-repository -y ppa:numix/ppa")
    os.system("add-apt-repository -y ppa:mpstark/elementary-tweaks-daily")
    os.system("apt-get update -y")
    os.system("apt-get install -y numix-gtk-theme numix-icon-theme-circle elementary-tweaks")

if keys == 'y' or keys == 'Y':
    os.system("apt-get install -y xbindkeys xdotool")
    # Map Super_L to the Search key
    # Create .xmodmap
    if model == "2":
        map = open("/home/" + username + "/.xmodmap", "w")
        map.write("""#!/bin/bash
xmodmap -e "keycode 225 = Super_L";
xmodmap -e “add mod4 = Super_L”;""")
        map.close()
        os.system("chmod +x ~/.xmodmap")
        os.system("ln -s ~/.xmodmap /etc/xdg/autostart/")

    # Remap all remaining top row keys and Delete to Shift+Backspace
    # Create .xbindkeysrc
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

if openJ == 'y' or openJ == 'Y':
    os.system("apt-get install -y openjdk-7-jdk")

if keys == 'y' or keys == 'Y':
    os.system("add-apt-repository -y ppa:linrunner/tlp")
    os.system("apt-get update -y")
    os.system("apt-get install -y tlp tlp-rdw")

if chrome == 'y' or chrome == 'Y':
    print("Downloading Chrome. This may take a few moments...")
    if platform.architecture()[0] == "64bit":
        kernel.retrieve("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", "/home/" + username + "/Downloads/google-chrome-stable_current_amd64.deb")
    else:
        kernel.retrieve("https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb", "/home/" + username + "/Downloads/google-chrome-stable_current_i386.deb")
    os.system("dpkg -i ~/Downloads/*.deb")
    os.system("rm ~/Downloads/*.deb")
    os.system("mv /usr/share/applications/google-chrome.desktop /usr/share/applications/google-chrome-stable.desktop")

if gimp == 'y' or gimp == 'Y':
    os.system("apt-get install -y gimp")

if libre == 'y' or libre == 'Y':
    os.system("apt-get install -y libreoffice")

if vlc == 'y' or vlc == 'Y':
    os.system("apt-get install -y vlc")

if bit == 'y' or bit == 'Y':
    os.system("apt-get install -y qbittorrent")

if glipper == 'y' or glipper == 'Y':
    os.system("apt-get install -y glipper")

if scroll == 'y' or scroll == 'Y':
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

# Restart the system
raw_input("Your system will now reboot so that all changes can take effect. Thanks for using my script and to all those who offered suggestions")
os.system("reboot")