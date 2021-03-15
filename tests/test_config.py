# ------------------------------------------------------------------------------
# Copyright (c) 2021, Mike Babst
#
# Distributed under the terms of the MIT License
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import os
from pathlib import Path

from dnaapp.config import AppConfig


def test_app_config():

    cfgdir = Path('.tmpdir').resolve()
    if not cfgdir.is_dir():
        os.mkdir(str(cfgdir))

    config_file = cfgdir / 'config.json'

    cfg = AppConfig(config_file)
    print(cfg.options)
    cfg.save()

