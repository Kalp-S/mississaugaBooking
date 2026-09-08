#!/usr/bin/env python3
"""
Active Mississauga 24/7 Scheduling Daemon
Monitors scheduling windows and executes automated reservations at 6:01 AM.
"""

import datetime
import sys
import time
import script

RIVER_GROVE_URL = "https://activemississauga.ca/#!registered-programs?search=2020%20badminton%20river%20grove"
MISSISSAUGA_VALLEY_URL = "https://activemississauga.ca/#!registered-programs?search=2020%20badminton%20mississauga%20valley"


def print_usage():
    print("Usage: python3 topLevel.py <CLIENT_BARCODE_1> <ACCOUNT_PIN_1> [<CLIENT_BARCODE_2> <ACCOUNT_PIN_2> ...]")
    print("       python3 topLevel.py --run-once <CLIENT_BARCODE> <ACCOUNT_PIN> [river_grove|valley]")
    print("\nOptions:")
    print("  --run-once       Execute booking sequence immediately for testing without waiting for 6:01 AM")
    print("  --help, -h       Show this help message")


def run_now(args):
    if len(args) < 4:
        print("[ERROR] Missing arguments for --run-once.")
        print_usage()
        return 1
    barcode = args[2]
    pin = args[3]
    location = args[4].lower() if len(args) > 4 else "river_grove"
    target_url = MISSISSAUGA_VALLEY_URL if "valley" in location else RIVER_GROVE_URL

    print("[INFO] Executing immediate booking test...")
    print("[INFO] Target: " + str(target_url))
    print("[INFO] Account Barcode: " + str(barcode))
    script.call(barcode, pin, target_url)
    return 0


def main(args):
    if len(args) < 2 or "--help" in args or "-h" in args:
        print_usage()
        return 0

    if args[1] == "--run-once":
        return run_now(args)

    if (len(args) - 1) % 2 != 0:
        print("[ERROR] Credentials must be provided in pairs: <Barcode> <PIN>")
        print_usage()
        return 1

    print("[INFO] Active Mississauga automated booking daemon started.")
    print("[INFO] Tracking accounts: " + str((len(args) - 1) // 2))
    print("[INFO] Waiting for target scheduling slots (06:01 AM)...")

    flagTue = False
    flagFri = False
    flagSat = False

    while True:
        check = datetime.datetime.now()
        weekday = int(check.weekday())
        hour = int(check.hour)
        minute = int(check.minute)

        # Reset daily trigger flags at midnight
        if hour == 0 and minute <= 5:
            flagTue = False
            flagFri = False
            flagSat = False

        # Schedule criteria:
        # Tuesday / Wednesday slot (weekday 1 or 2 at 6:01+ AM)
        # Friday slot (weekday 4 at 6:01+ AM)
        # Saturday / Sunday slot (weekday 5 or 6 at 6:01+ AM)
        tue_cond = (weekday in (1, 2)) and hour >= 6 and minute >= 1 and (not flagTue)
        fri_cond = (weekday == 4) and hour >= 6 and minute >= 1 and (not flagFri)
        sat_cond = (weekday in (5, 6)) and hour >= 6 and minute >= 1 and (not flagSat)

        if tue_cond or fri_cond or sat_cond:
            if tue_cond or sat_cond:
                target_url = RIVER_GROVE_URL
                print("[TRIGGER] Running Tuesday/Saturday schedule at: " + str(check))
                for x in range(1, len(args), 2):
                    try:
                        script.call(args[x], args[x + 1], target_url)
                    except Exception as e:
                        print("[ERROR] Failed to book account " + str(args[x]) + ": " + str(e))

                if weekday in (1, 2):
                    flagTue = True
                    flagFri = False
                    flagSat = False
                else:
                    flagTue = False
                    flagFri = False
                    flagSat = True
            else:
                target_url = MISSISSAUGA_VALLEY_URL
                print("[TRIGGER] Running Friday schedule at: " + str(check))
                for x in range(1, len(args), 2):
                    try:
                        script.call2(args[x], args[x + 1], target_url)
                    except Exception as e:
                        print("[ERROR] Failed to book account " + str(args[x]) + ": " + str(e))

                flagTue = False
                flagFri = True
                flagSat = False

        # Sleep to avoid high CPU spin in daemon mode
        time.sleep(30)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
