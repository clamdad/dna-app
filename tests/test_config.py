# ------------------------------------------------------------------------------
# Copyright (c) 2021, Mike Babst
#
# Distributed under the terms of the MIT License
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from dnaapp.config import AppConfig


def test_app_config():
    cfg = AppConfig('.tmpdir/config.json')
    print(cfg.options)
    cfg.save()
