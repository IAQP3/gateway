# Setup

Two Python Bluetooth Libraries are needed: pygatt and pygattlib

Pygatt and it’s installation instructions can be found here:
https://github.com/peplin/pygatt

Pygattlib and it’s installation instructions can be found here:
https://bitbucket.org/OscarAcena/pygattlib


# Install dependencies:
sudo apt-get install libboost-python-dev libboost-thread-dev libbluetooth-dev libglib2.0-dev -y

# Install libraries:
sudo pip install pygatt gattlib pexpect

# Run:
sudo python main.py
