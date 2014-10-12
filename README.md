There are two scripts here to help apply a large amount of hot fixes for elementary OS Luna and Frey on the HP Chromebook 14. This script should work for many other Chromebooks, but I've only tested it on my HP 14 for Luna.

Script elementary12.py is for Luna with prompts to select installed software

Script elementary12_streamed.py is for Luna and eliminates most prompts and just installs everything. See below for the full list of fixes and installations

Script elementary14.py is for Freya with prompts to select installed software

# Usage: #
1. Install elementary OS Luna/Freya using Chrubuntu to partition the drive and then a live USB containing elementary OS Luna/Freya

2. Once installed, download the script and run the command from terminal: "sudo python ~/Downloads/elementary12.py"

3. Be sure to carefully type your username given during installation as this will be relied upon in the script

4. Follow along with the script reading each prompt carefully

5. If the script fails or you accidentally stop it, I don't have any good remedies besides looking at one of my manual guides. DON'T RUN IT A 2ND TIME NO MATTER WHAT

# After the script has finished and your system has rebooted you can optionally do the following: #

1. Assign a hotkey to Guake if you installed it using Guake Preferences ($ guake -p) as the default one won't work on Chromebooks

2. (Luna) Set your themes and wingpanel settings in Elementary Tweaks from in the System Settings if you chose to install them

3. Delete your wired connection from Network Manager to avoid it trying to connect to it all the time. Hoping to add this to the script soon.

4. Assign Fullscreen (F4) to Toggle Fullscreen in System Settings>Keyboard>Windows>Shortcuts (Luna doesn't have anything mapped to Toggle Fullscreen by default. Not sure about Luna but will look into finding the conf file for this and adding it to the script)

5. Enjoy elementary OS



Ian Richardson / iantrich.com



Tweaks / Installations:

* Upgrade kernel to stable 3.17

* Fix suspend and boot times

* Set power button to function as expected (Freya)

* Touchpad tweaks (Luna: Increased sensitivity Freya: ChromeOS driver)

* Upgrade Xserver for better performance (Luna)

* Install Oracle JDK 7 or OpenJDK 7

* Install Guake Terminal

* Install git

* Install Numix theme, icons and elementary tweaks

* Install Wingpanel-Super and Wingpanel-Slim (Luna)

* Install Build Essentials

* Install Keymapping Tools

* Install TLP Battery Saving Tool

* Install Chrome browser and fix Plank icon issue

* Remap Super key to Search key (Search+Space for Application Launcher)

* Remap Left, Right, Refresh, Fullscreen, Display, Brightness and Volume Keys

* Map Delete to Shift+Backspace

* Install Gimp

* Install Libreoffice

* Install VLC

* Install qBittorrent

* Install Glipper Clipboard Manager

* Install Natural Scrolling (OS X Style Scrolling) (Both, but more applicable for Freya as the ChromeOS touchpad driver disables touchpad settings in System Settings)