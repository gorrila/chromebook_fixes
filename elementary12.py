#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ian Richardson'

# You must run this file as superuser

import urllib
import os
import fileinput
import sys

print("Script made by Ian Richardson; iantrich.com for public use")
print("I take no responsibility should anything go wrong while using this script.")
cont = raw_input("Use at your own risk. Do you wish to continue? [Y/n] ")
if cont is not 'y' and cont is not 'Y':
    exit()

input("Please connect to internet service before continuing. Hit Enter when ready...")

username = raw_input("Carefully enter your username: ")

#print("Grabbing kernel 3.17 stable...may take a few moments")
kernel = urllib.URLopener()
kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb", "/home/" + username + "/Downloads/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb")
kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700_3.17.0-031700.201410060605_all.deb", "/home/" + username + "/Downloads/linux-headers-3.17.0-031700_3.17.0-031700.201410060605_all.deb")
kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb", "/home/" + username + "/Downloads/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb")

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

guake = raw_input("Install Guake: A dropdown terminal? [Y/n]? ")
if guake is 'y' or guake is 'Y':
    os.system("apt-get install guake")

numix = raw_input("Install the beautiful numix theme and elementary tweaks? [Y/n]? ")
if numix is 'y' or numix is 'Y':
    os.system("add-apt-repository ppa:numix/ppa")
    os.system("add-apt-repository ppa:versable/elementary-update")
    os.system("apt-get update")
    os.system("apt-get install numix-gtx-theme numix-icon-theme-circle elementary-tweaks")

wing = raw_input("Install slim and super wingpanel? If you don't know what they are look it up. [Y/n} ")
if wing is 'y' or wing is 'Y':
    os.system("add-apt-repository ppa:numix/ppa")
    os.system("add-apt-repository ppa:versable/elementary-update")
    os.system("apt-get update")
    os.system("apt-get install wingpanel-slim super-wingpanel")

keys = raw_input("Remap Left, Right, Refresh, Display, Window, Search(Super_L) and Shift+Backspace(Delete) to function properly? The Search button will only be properly mapped on the HP 14. [Y/n]? ")
if keys is 'y' or keys is 'Y':
    os.system("apt-get install xbindkeys xdotool")
    # Map Super_L to the Search key
    # Create .xmodmap
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
shift+BackSpace""")
    os.system("chmod +x ~/.xbindkeysrc")

java = raw_input("Install Oracle Java 7? [Y/n]? ")
if java is 'y' or java is 'Y':
    print("Follow the on-screen instructions to finish the installation. It might take awhile")
    os.system("add-apt-repository ppa:webupd8team/java")
    os.system("apt-get update")
    os.system("apt-get install python-software-properties oracle-java7-installer")
else:
    java = raw_input("Install Open JDK 7? [Y/n]? ")
    if java is 'y' or java is 'Y':
        os.system("apt-get install openjdk-7-jdk")

battery = raw_input("Install TLP Battery Saver? [Y/n]? ")
if keys is 'y' or keys is 'Y':
    os.system("add-apt-repository ppa:linrunner/tlp")
    os.system("apt-get update")
    os.system("apt-get install tlp tlp-rdw")

chrome = raw_input("Install Chrome browser? [Y/n]? ")
if chrome is 'y' or chrome is 'Y':
    print("Downloading Chrome. This may take a few moments...")
    kernel.retrieve("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", "/home/" + username + "/Downloads/google-chrome-stable_current_amd64.deb")
    os.system("dpkg -i ~/Downloads/google-chrome-stable_current_amd64.deb")
    os.system("rm ~/Downloads/google-chrome-stable_current_amd64.deb")
    os.system("mv /usr/share/applications/google-chrome.desktop /usr/share/applications/google-chrome-stable.desktop")

gimp = raw_input("Install GIMP image editor? [Y/n]? ")
if gimp is 'y' or gimp is 'Y':
    os.system("apt-get install gimp")

libre = raw_input("Install LibreOffice Suite? [Y/n]? ")
if libre is 'y' or libre is 'Y':
    os.system("apt-get install libreoffice")

vlc = raw_input("Install VLC media player? [Y/n]? ")
if vlc is 'y' or vlc is 'Y':
    os.system("apt-get install vlc")

bit = raw_input("Install qBittorrent? [Y/n]? ")
if bit is 'y' or bit is 'Y':
    os.system("apt-get install qbittorrent")

glipper = raw_input("Install glipper clibboard manager? [Y/n]? ")
if glipper is 'y' or glipper is 'Y':
    os.system("apt-get install glipper")

scroll = raw_input("Install OS X style natural scrolling? [Y/n]? ")
if scroll is 'y' or scroll is 'Y':
    os.system("add-apt-repository ppa:zedtux/naturalscrolling")
    os.system("apt-get update")
    os.system("apt-get install naturalscrolling")
    os.system(" ln -s /usr/share/applications/naturalscrolling.desktop /etc/xdg/autostart/")

input("Making partitions on USBs and SD Cards writable. You'll still need to change permissions in Properies. Hit Enter...")
os.system("gksudo pantheon-files")

print("Checking for any updates")
os.system("apt-get upgrade")
os.system("apt-get dist-upgrade")

print("Removing leftovers")
os.system("apt-get autoremove")

# Restart the system
input("Your system will now reboot so that all changes can take effect. Thanks for using my script")
os.system("reboot")
