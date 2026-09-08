#!/usr/bin/env python3
"""
Booking execution wrapper for Mississauga active booking scripts.
"""

import automate


def call(arg1, arg2, arg3):
	"""Execute booking sequence for River Grove or Tuesday/Saturday sessions."""
	run = automate.Automate(arg1, arg2, arg3)
	run.runSequence()
	print("[COMPLETE] Successfully processed session for: " + str(arg1))


def call2(arg1, arg2, arg3):
	"""Execute booking sequence for Mississauga Valley or Friday sessions."""
	run = automate.Automate(arg1, arg2, arg3)
	run.runSequence()
	print("[COMPLETE] Successfully processed session for: " + str(arg1))
