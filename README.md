# yoacr - YubiKey OTP Access Code Remover
Remove access codes from YubiKey OTP slots when you have lost or forgotten the code.

## Prerequisites
Instructions for Ubuntu 20.04+
```
sudo apt install libusb-dev pcscd libpcsclite-dev libccid python3-dev python3-venv swig gcc python3-wheel git
git clone https://github.com/covertsh/yoacr.git
cd yoacr/
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

You are now ready to use ```yoacr```.

## Usage

1. Insert your YubiKey. Make sure you only have one YubiKey inserted.
2. In the ```yoacr``` directory, run ```python3 yoacr.py```.
3. Usage information will be printed:
```
usage: yoacr.py [-h] {1,2}
yoacr.py: error: the following arguments are required: slot
```
4. To find and remove the access code from slot 1:
```
python3 yoacr.py 1
```
Or to remove the code from slot 2:
```
python3 yoacr.py 2
```

## Tips
There is a shortcut: often, the access code is set to the YubiKey serial number because this is offered as an option in the 
YubiKey Personalization Tool. This will be tried first.

If a full brute-force search is needed, you will see the current code being tried on your screen. The search can take a very, very 
long time. YubiKeys can handle approximately 27 attempts per second and the search cannot be parallelized.
