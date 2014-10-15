__author__ = 'sinan.boecker'


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
