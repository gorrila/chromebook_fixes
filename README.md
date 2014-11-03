This script is here to help apply a large amount of hot fixes for Linux on Chromebooks.

# Supported Distros: #
* Ubuntu 12.xx based
* Ubuntu 14.04 based
* elementary OS 0.2 Luna
* elementary OS 0.3 Freya

# Supported Chromebooks: #
* Acer C720
* HP Chromebook 14

Other Distros and Chromebooks should also work but are untested.

# Usage: #
1. Install elementary OS Luna/Freya using Chrubuntu to partition the drive and a live USB containing elementary OS Luna/Freya.

2. Once installed, download the script and run the command from terminal: "sudo python ~/Downloads/elementary.py".

3. Be sure to carefully type your username during installation as this will be relied upon in the script.

4. Follow along with the script reading each prompt carefully.

5. If the script fails or you accidentally stop it, I don't have any good remedies besides looking at one of my manual guides or reinstalling and starting over. DON'T RUN IT A 2ND TIME NO MATTER WHAT

# After the script has finished and your system has rebooted you can optionally do the following: #

1. (Luna) Delete your wired connection from Network Manager to avoid it trying to connect to it all the time. Hoping to add this to the script soon.

2. (Freya) Set the power button configuration. Open System Settings->Power and set Power Button to ”Ask Me”.

3. (Luna/Freya with Chrome) Open Chrome and in the address bar enter “chrome://flags” and enable “Override software rendering list”.

4. (Luna/Freya) Set your themes and wingpanel (Luna Only) settings in Elementary Tweaks from in the System Settings if you chose to install them.

5. (Luna/Freya with Guake) Assign a hotkey using Guake Preferences ($ guake -p) as the default one won't work on Chromebooks. (Note that there is a bug in Guake that hotkeys with Ctrl in them won't fire correctly)

6. Enjoy elementary OS




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

# Known Issues: #
(Freya on C720) - Wake from sleep causes problems.
