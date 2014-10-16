__author__ = 'sinan.boecker'

import urllib
import os
import platform
import subprocess
import getpass


def install_3_17():
    update_kernel = False

    # Check if kernel is up to date
    if '3.17.0-031700-generic' in subprocess.Popen(["uname", "-r"], stdout=subprocess.PIPE).communicate()[0]:
        update_kernel = True

    if update_kernel:
        print("Grabbing kernel 3.17 stable...may take a few moments")
        kernel = urllib.URLopener()
        # Check if system is 32 or 64-bit
        if platform.architecture()[0] is "64bit":
            kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb", "/tmp/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb")
            kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb", "/tmp/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_amd64.deb")
        else:
            kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_i386.deb", "/tmp/linux-headers-3.17.0-031700-generic_3.17.0-031700.201410060605_i386.deb")
            kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_i386.deb", "/tmp/linux-image-3.17.0-031700-generic_3.17.0-031700.201410060605_i386.deb")
        kernel.retrieve("http://kernel.ubuntu.com/~kernel-ppa/mainline/v3.17-utopic/linux-headers-3.17.0-031700_3.17.0-031700.201410060605_all.deb", "/tmp/linux-headers-3.17.0-031700_3.17.0-031700.201410060605_all.deb")

        print("Remove old kernel")
        os.system("""apt-get remove --purge $(dpkg -l 'linux-image-*' | sed '/^ii/!d;/'"$(uname -r | sed "s/\(.*\)-\([^0-9]\+\)/\1/")"'/d;s/^[^ ]* [^ ]* \([^ ]*\).*/\1/;/[0-9]/!d')""")

        print("Extract packages to update the kernel")
        os.system("dpkg -i /tmp/linux-headers-3.17*.deb")
        os.system("dpkg -i /tmp/linux-image-3.17*.deb")

        os.system("rm /tmp/linux-headers-3.17*.deb")
        os.system("rm /tmp/linux-image-3.17*.deb")