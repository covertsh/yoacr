#!/usr/bin/env python3

import argparse

try:
    from yubikit.yubiotp import YubiOtpSession, SLOT, UpdateConfiguration
    from ykman import scripting as s
    from yubikit.core.otp import CommandRejectedError
except ImportError:
    print("Please ensure you have installed the prerequisites.")
    exit()

parser = argparse.ArgumentParser("yoacr.py")
parser.add_argument(
    "slot", help="Which slot to remove the access code from.", type=int, choices=[1, 2]
)
args = parser.parse_args()

try:
    device = s.single()
except ValueError as e:
    if str(e) != "Failed to get single YubiKey":
        raise
    else:
        print("Please ensure only one YubiKey is connected to your computer.")
        exit()

try:
    session = YubiOtpSession(device.otp())
except ValueError as e:
    if str(e) != "Unsupported Connection type":
        raise
    else:
        print("Could not open OTP connection. Are you sure the OTP applet is enabled?")
        exit()

slot_configured = session.get_config_state().is_configured(slot=args.slot)

if not slot_configured:
    print(f"OTP slot {args.slot} is not configured. There is no access code.")
    exit()

slot_names = [SLOT.ONE, SLOT.TWO]

try:
    session.update_configuration(
        slot=slot_names[args.slot - 1],
        cur_acc_code=(0).to_bytes(6, byteorder="big"),
        configuration=UpdateConfiguration(),
    )
    print(f"No access code was set.")
    exit()
except CommandRejectedError:
    pass

try:
    serial_as_hex = bytes.fromhex(f"{device.info.serial:#0{12}d}")
    session.update_configuration(
        slot=slot_names[args.slot - 1],
        cur_acc_code=serial_as_hex,
        configuration=UpdateConfiguration(),
    )
    print(
        f"Access code was {device.info.serial} (used device serial number). Code removed."
    )
    exit()
except CommandRejectedError:
    pass

print("Tried empty access code and device serial number. Starting brute force search.")
test_acc_code = 0

while test_acc_code <= 2 << 48:
    print(f"\rTrying code: 0x{test_acc_code:0>12x}", end="")
    try:
        session.update_configuration(
            slot=slot_names[args.slot - 1],
            cur_acc_code=test_acc_code.to_bytes(6, byteorder="big"),
            configuration=UpdateConfiguration(),
        )
        print(f"\nAccess code was 0x{test_acc_code:0>12x}. Code removed.")
        exit()
    except CommandRejectedError:
        test_acc_code += 1
