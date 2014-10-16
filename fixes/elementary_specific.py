__author__ = 'sinan.boecker'

import os


def elementary_tweaks(distro_version):
    eos_tweaks = raw_input("Install elementary tweaks? [Y/n]? ")
    if eos_tweaks == 'y' or eos_tweaks == 'Y':
        if distro_version == "0.2":
            os.system("add-apt-repository -y ppa:versable/elementary-update")
        elif distro_version == "0.3":
            os.system("add-apt-repository -y ppa:mpstark/elementary-tweaks-daily")

        os.system("apt-get update -y")
        os.system("apt-get install -y elementary-tweaks")


def numix():
    numix = raw_input("Install the numix theme? [Y/n]? ")
    if numix == 'y' or numix == 'Y':
        os.system("add-apt-repository -y ppa:numix/ppa")
        os.system("apt-get update -y")
        os.system("apt-get install -y numix-gtk-theme numix-icon-theme-circle")


def wingpanel():
    wing = raw_input("Install slim and super wingpanel? If you don't know what they are look it up. [Y/n} ")
    if wing == 'y' or wing == 'Y':
        os.system("add-apt-repository -y ppa:versable/elementary-update")
        os.system("apt-get update -y")
        os.system("apt-get install -y wingpanel-slim super-wingpanel")
