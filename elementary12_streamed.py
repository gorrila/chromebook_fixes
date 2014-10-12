#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Ian Richardson'

# You must run this file as superuser

import urllib
import os
import fileinput
import sys

print("Script made by Ian Richardson / iantrich.com, for public use")
print("I take no responsibility should anything go wrong while using this script.")
cont = raw_input("Use at your own risk. Do you wish to continue? [Y/n] ")
if cont is not 'y' and cont is not 'Y':
    exit()

raw_input("Please connect to internet service before continuing. Hit Enter when ready...")

username = raw_input("Carefully enter your username: ")

raw_input("You'll need to interact for the small portion where Java is installed and then should be able to leave and come back once it's finished. About 30 minutes or so depending on your internet connection...Enter")

# Install Java
os.system("add-apt-repository -y ppa:webupd8team/java")
os.system("apt-get update -y")
os.system("apt-get install -y python-software-properties oracle-java7-installer")

print("Grabbing kernel 3.17 stable...may take a few moments")
kernel = urllib.URLopener()
kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb", "/home/" + username + "/Downloads/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb")
kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700_3.17.0-031700.201410060605_all.deb", "/home/" + username + "/Downloads/linux-headers-3.17.0-031700_3.17.0-031700.201410060605_all.deb")
kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb", "/home/" + username + "/Downloads/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb")

print("Remove old kernel")
os.system("""apt-get remove -y --purge $(dpkg -l 'linux-image-*' | sed '/^ii/!d;/'"$(uname -r | sed "s/\(.*\)-\([^0-9]\+\)/\1/")"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d')""")

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

# Upgrade Xserver for better performance
os.system("apt-get install -y xserver-xorg-lts-trusty")

# Install Guake
os.system("apt-get install -y guake")
os.system("ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/")

# Install numix, elementary tweaks and wingpanels
os.system("add-apt-repository -y ppa:numix/ppa")
os.system("add-apt-repository -y ppa:versable/elementary-update")
os.system("apt-get update -y")
os.system("apt-get install -y numix-gtk-theme numix-icon-theme-circle elementary-tweaks")
os.system("apt-get install wingpanel-slim super-wingpanel")

# Remap keys
os.system("apt-get install -y xbindkeys xdotool")
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

# Install tlp battery manager
os.system("add-apt-repository -y ppa:linrunner/tlp")
os.system("apt-get update -y")
os.system("apt-get install -y tlp tlp-rdw")

# Install Chrome browser
print("Downloading Chrome. This may take a few moments...")
kernel.retrieve("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", "/home/" + username + "/Downloads/google-chrome-stable_current_amd64.deb")
os.system("dpkg -i ~/Downloads/google-chrome-stable_current_amd64.deb")
os.system("rm ~/Downloads/google-chrome-stable_current_amd64.deb")
os.system("mv /usr/share/applications/google-chrome.desktop /usr/share/applications/google-chrome-stable.desktop")

# Install gimp
os.system("apt-get install -y gimp")

# Install LibreOffice
os.system("apt-get install -y libreoffice")

# Install VLC
os.system("apt-get install -y vlc")

# Install qBittorrent
os.system("apt-get install -y qbittorrent")

# Install glipper
os.system("apt-get install -y glipper")

# Install Natural Scrolling
os.system("add-apt-repository -y ppa:zedtux/naturalscrolling")
os.system("apt-get update -y")
os.system("apt-get install -y naturalscrolling")
os.system(" ln -s /usr/share/applications/naturalscrolling.desktop /etc/xdg/autostart/")

print("Checking for any updates")
os.system("apt-get upgrade -y")
os.system("apt-get dist-upgrade -y")

print("Removing leftovers")
os.system("apt-get autoremove -y")

# Restart the system
raw_input("Hit Enter to Reboot")
os.system("reboot")
