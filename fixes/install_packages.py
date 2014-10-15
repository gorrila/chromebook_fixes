__author__ = 'sinan.boecker'

import os
import platform


def install_additional_packages(install_mode):
    if install_mode is '1':
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
        if java is not 'y' and java is not 'Y':
            openJ = raw_input("Install Open JDK 7? [Y/n]? ")
    else:
        guake = git = battery = chrome = gimp = libre = vlc = bit = glipper = scroll = java = 'y'

    if guake is 'y' or guake is 'Y':
        os.system("apt-get install -y guake")
        os.system("ln -s /usr/share/applications/guake.desktop /etc/xdg/autostart/")

    if git is 'y' or git is 'Y':
        os.system("apt-get install -y git")

    if openJ is 'y' or openJ is 'Y':
        os.system("apt-get install -y openjdk-7-jdk")

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

    if java is 'y' or java is 'Y':
        raw_input("Follow the on-screen instructions to finish the Java installation. It might take awhile, but this is the last prompt from me")
        os.system("add-apt-repository -y ppa:webupd8team/java")
        os.system("apt-get update -y")
        os.system("apt-get install -y python-software-properties oracle-java7-installer")

    if battery is 'y' or battery is 'Y':
        os.system("add-apt-repository -y ppa:linrunner/tlp")
        os.system("apt-get update -y")
        os.system("apt-get install -y tlp tlp-rdw")


    if scroll is 'y' or scroll is 'Y':
        os.system("add-apt-repository -y ppa:zedtux/naturalscrolling")
        os.system("apt-get update -y")
        os.system("apt-get install -y naturalscrolling")
        os.system(" ln -s /usr/share/applications/naturalscrolling.desktop /etc/xdg/autostart/")