__author__ = 'sinan.boecker'

import os
import fileinput
import sys
import subprocess
import getpass


def apply_general_fixes():
    #fix_suspend()
    #fix_rclocal()
    fix_unbindehci()
    create_udev_rule()
    fix_grub()


def create_udev_rule():
    udev = open("/etc/udev/rules.d/10_disable-ehci.rules", 'w+')
    udev.write("""ACTION=="add", SUBSYSTEM=="pci", DRIVER=="ehci_hcd", \
    RUN+="/bin/sh -c 'echo -n %k > %S%p/driver/unbind'""""")

    os.system("update-initramfs -k all -u")


def fix_unbindehci():
    ehci = open("/etc/initramfs-tools/scripts/init-top/unbind_ehci", 'w+')
    ehci.write("""#####################
    #!/bin/sh
    PREREQ=""

    prereqs()
    {
            echo "${PREREQ}"
    }

    case ${1} in
            prereqs)
                    prereqs
                    exit 0
                    ;;
    esac

    log_success_msg "Unbind ehci for preventing error"
    echo -n "0000:00:1d.0" > /sys/bus/pci/drivers/ehci-pci/unbind
    exit 0
    #################""")
    ehci.close()
    os.system("chmod a+x /etc/initramfs-tools/scripts/init-top/unbind_ehci")


def fix_suspend():
    print("Fix suspend and boot times")
    sound = open("/etc/pm/sleep.d/05_Sound", "w+")
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
            sys.stdout.write("""GRUB_CMDLINE_LINUX_DEFAULT="quiet splash add_efi_memmap boot=local noresume noswap i915.semaphores=0 i915.modeset=1 i915.use_mmio_flip=1 i915.powersave=1 i915.enable_ips=1 i915.disable_power_well=1 i915.enable_hangcheck=1 i915.enable_cmd_parser=1 i915.fastboot=0 i915.enable_ppgtt=1 i915.reset=0 i915.lvds_use_ssc=0 i915.enable_psr=0 drm.debug=0 drm.vblankoffdelay=1 tpm_tis.force=1 tpm_tis.interrupts=0 nmi_watchdog=panic,lapic\"""")

    os.system("update-grub")
    os.system("update-grub2")


def fix_mediakeys(username):
        # Remap all remaining top row keys and Delete to Shift+Backspace
        # Create .xbindkeysrc
        xbind = open("/home/" + username + "/.xbindkeysrc", "w+")
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


def adjust_touchpad_sensitivity():
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


def install_chromeos_touchpad_drivers():
    driver = raw_input("Install ChromeOS touchpad driver? [Y/n]? ")
    if driver is 'y' or driver is 'Y':
        if not subprocess.Popen(["[ -f /usr/share/X11/xorg.conf.d/50-touchpad-cmt-peppy.conf]", ""], stdout=subprocess.PIPE).communicate()[0]:
            os.system("add-apt-repository -y ppa:hugegreenbug/cmt")
            os.system("apt-get update -y")
            os.system("apt-get install -y libevdevc libgestures  xf86-input-cmt")
            os.system("mv /usr/share/X11/xorg.conf.d/50-synaptics.conf /usr/share/X11/xorg.conf.d/50-synaptics.conf.old")
            os.system("cp /usr/share/xf86-input-cmt/50-touchpad-cmt-peppy.conf /usr/share/X11/xorg.conf.d/")


def upgrade_xserver():
    print("Upgrade Xserver for better performance")
    os.system("apt-get install -y xserver-xorg-lts-trusty")
