__author__ = 'sinan.boecker'

import os
import fileinput
import sys


def fix_suspend():
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


def fix_rclocal():
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


def fix_grub():
    # Edit grub and update
    for line in fileinput.input("/etc/default/grub", inplace=True):
        if "GRUB_CMDLINE_LINUX_DEFAULT" not in line:
            sys.stdout.write(line)
        else:
            sys.stdout.write("""GRUB_CMDLINE_LINUX_DEFAULT="quiet splash add_efi_memmap boot=local noresume noswap i915.modeset=1 tpm_tis.force=1 tpm_tis.interrupts=0 nmi_watchdog=panic,lapic\"""")
    os.system("update-grub")
    os.system("update-grub2")


def fix_mediakeys():
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
