# HowToInstall MOG-DOS

## PC: (Windows 10/11, probably works on Linux too)
- Install Python 3.11 or newer: https://apps.microsoft.com/detail/9nrwmjp3717k?hl=en-us&gl=US
- Go to cmd/terminal and copy paste this(these libraries): ``pip install tk customtkinter``
*(it uses all of these libraries socket, threading, time, random, tkinter.)*
- **Now you can open any of the versions of the MOG-DOS projects.**

## How to use
- Input the IP
- The port you should use is ``80``
- Type the number of threads. (that your CPU has/handles)
- Input the seconds (time) for how much you want to run. **(isn't in the classic V1 and V2, only in V1.1)**
- Select the attack e.g TCP, UDP, HTTP and etc. **(isn't available in every version)**

# How to use in ANDROID (Only the classic V1 available for Android)
- Go to GooglePlay-Store and download **Termux**
- After it downloads **go to Termux** and copy and paste this: ``pkg update -y && pkg upgrade -y && pkg install python -y && termux-setup-storage``
- After it installs all of the packages and etc. it will open a window asking for permissions to your storage so find termux and give them the permission.
- To open the python file now you should copy paste this: ``cd /storage/emulated/0/Download/`` and then ``python example.py`` (to open V1 type this ``python  MOG-DOS_V1.py``)
