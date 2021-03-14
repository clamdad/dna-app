# ------------------------------------------------------------------------------
# Copyright (c) 2021, Mike Babst
#
# Distributed under the terms of the MIT License
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from dnaapp.home import AppHomeDirectory


def test_app_home():
    ah = AppHomeDirectory('myapp')
    print(ah)
