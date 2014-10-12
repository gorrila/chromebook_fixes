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
cont = input("Use at your own risk. Do you wish to continue? [Y/n] ")
if cont is not 'y' and cont is not 'Y':
    exit()

input("Please connect to internet service before continuing. Hit Enter when ready...")

username = input("Carefully enter your username: ")

print("What model do you have?\n1. C720\n2. HP 14\n3. Other")
model = input("")

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

print("Adjust power button settings.")
input("Be sure to go to System Settings>Power>Power Button and change to 'Ask Me'. Hit Enter to continue...")
# Edit logind.conf
for line in fileinput.input("/etc/systemd/logind.conf"):
    if "Handlepowerkey" not in line:
        sys.stdout.write(line)
    else:
        sys.stdout.write("Handlepowerkey=ignore")

driver = input("Install ChromeOS touchpad driver? [Y/n]? ")
if driver is 'y' or driver is 'Y':
    os.system("add-apt-repository -y ppa:hugegreenbug/cmt")
    os.system("apt-get update -y")
    os.system("apt-get install -y libevdevc libgestures  xf86-input-cmt")
    os.system("mv /usr/share/X11/xorg.conf.d/50-synaptics.conf /usr/share/X11/xorg.conf.d/50-synaptics.conf.old")
    os.system("cp /usr/share/xf86-input-cmt/50-touchpad-cmt-peppy.conf /usr/share/X11/xorg.conf.d/")

guake = input("Install Guake: A dropdown terminal? [Y/n]? ")
if guake is 'y' or guake is 'Y':
    os.system("apt-get install -y guake")
    os.system("ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/")

numix = input("Install the beautiful numix theme and elementary tweaks? [Y/n]? ")
if numix is 'y' or numix is 'Y':
    os.system("add-apt-repository -y ppa:numix/ppa")
    os.system("add-apt-repository -y ppa:mpstark/elementary-tweaks-daily")
    os.system("apt-get update -y ")
    os.system("apt-get install -y numix-gtk-theme numix-icon-theme-circle elementary-tweaks")

keys = input("Remap Left, Right, Refresh, Display, Window, Search(Super_L) and Shift+Backspace(Delete) to function properly? The Search button will only be properly mapped on the HP 14. [Y/n]? ")
if keys is 'y' or keys is 'Y':
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

java = input("Install Oracle Java 7? [Y/n]? ")
if java is 'y' or java is 'Y':
    print("Follow the on-screen instructions to finish the installation. It might take awhile")
    os.system("add-apt-repository -y ppa:webupd8team/java")
    os.system("apt-get update -y")
    os.system("apt-get install -y python-software-properties oracle-java7-installer")
else:
    java = input("Install Open JDK 7? [Y/n]? ")
    if java is 'y' or java is 'Y':
        os.system("apt-get install -y openjdk-7-jdk")

git = input("Install git? [Y/n] ")
if git is 'y' or git is 'Y':
    os.system("apt-get install -y git")

battery = input("Install TLP Battery Saver? [Y/n]? ")
if keys is 'y' or keys is 'Y':
    os.system("add-apt-repository -y ppa:linrunner/tlp")
    os.system("apt-get update -y")
    os.system("apt-get install -y tlp tlp-rdw")

chrome = input("Install Chrome browser? [Y/n]? ")
if chrome is 'y' or chrome is 'Y':
    print("Downloading Chrome. This may take a few moments...")
    if platform.architecture()[0] is "64bit":
        kernel.retrieve("https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb", "/home/" + username + "/Downloads/google-chrome-stable_current_amd64.deb")
    else:
        kernel.retrieve("https://dl.google.com/linux/direct/google-chrome-stable_current_i386.deb", "/home/" + username + "/Downloads/google-chrome-stable_current_amd64.deb")
    os.system("dpkg -i ~/Downloads/*.deb")
    os.system("rm ~/Downloads/*.deb")
    os.system("mv /usr/share/applications/google-chrome.desktop /usr/share/applications/google-chrome-stable.desktop")

gimp = input("Install GIMP image editor? [Y/n]? ")
if gimp is 'y' or gimp is 'Y':
    os.system("apt-get install -y gimp")

libre = input("Install LibreOffice Suite? [Y/n]? ")
if libre is 'y' or libre is 'Y':
    os.system("apt-get install -y libreoffice")

vlc = input("Install VLC media player? [Y/n]? ")
if vlc is 'y' or vlc is 'Y':
    os.system("apt-get install -y vlc")

bit = input("Install qBittorrent? [Y/n]? ")
if bit is 'y' or bit is 'Y':
    os.system("apt-get install -y qbittorrent")

glipper = input("Install glipper clibboard manager? [Y/n]? ")
if glipper is 'y' or glipper is 'Y':
    os.system("apt-get install -y glipper")

scroll = input("Install OS X style natural scrolling? [Y/n]? ")
if scroll is 'y' or scroll is 'Y':
    os.system("add-apt-repository -y ppa:zedtux/naturalscrolling")
    os.system("apt-get update -y")
    os.system("apt-get install -y naturalscrolling")
    os.system(" ln -s /usr/share/applications/naturalscrolling.desktop /etc/xdg/autostart/")

print("Checking for any updates")
os.system("apt-get upgrade -y ")
os.system("apt-get dist-upgrade -y ")

print("Removing leftovers")
os.system("apt-get autoremove -y")

# Restart the system
os.system("reboot")
