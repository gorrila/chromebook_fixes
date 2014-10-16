__author__ = 'sinan.boecker'

import os
import platform
import urllib


def install_additional_packages(install_mode, username):
    if install_mode == '1':
        guake = raw_input("Install Guake: A dropdown terminal? [Y/n]? ")
        git = raw_input("Install git? [Y/n] ")
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
        guake = git = battery = chrome = gimp = libre = vlc = bit = glipper = scroll = java = 'y'

    if guake == 'y' or guake == 'Y':
        os.system("apt-get install -y guake")
        os.system("ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/")

    if git == 'y' or git == 'Y':
        os.system("apt-get install -y git")

    if openJ == 'y' or openJ == 'Y':
        os.system("apt-get install -y openjdk-7-jdk")

    if chrome == 'y' or chrome == 'Y':
        print("Downloading Chrome. This may take a few moments...")
        kernel = urllib.URLopener()
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

    if java == 'y' or java == 'Y':
        raw_input("Follow the on-screen instructions to finish the Java installation. It might take awhile, but this is the last prompt from me")
        os.system("add-apt-repository -y ppa:webupd8team/java")
        os.system("apt-get update -y")
        os.system("apt-get install -y python-software-properties oracle-java7-installer")

    if battery == 'y' or battery == 'Y':
        os.system("add-apt-repository -y ppa:linrunner/tlp")
        os.system("apt-get update -y")
        os.system("apt-get install -y tlp tlp-rdw")


    if scroll == 'y' or scroll == 'Y':
        os.system("add-apt-repository -y ppa:zedtux/naturalscrolling")
        os.system("apt-get update -y")
        os.system("apt-get install -y naturalscrolling")
        os.system(" ln -s /usr/share/applications/naturalscrolling.desktop /etc/xdg/autostart/")