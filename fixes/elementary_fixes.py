__author__ = 'sinan.boecker'

import os
import subprocess

def elementary_fixes(username, distro, install_mode):
    if distro is 'luna':
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

    if distro is 'freya' or '14.04':
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