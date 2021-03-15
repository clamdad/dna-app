# ------------------------------------------------------------------------------
# Copyright (c) 2021, Mike Babst
#
# Distributed under the terms of the MIT License
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

import logging
import os
from pathlib import Path

import pytest

import dnaapp.logs
from dnaapp.logs import _console_handler_name, _file_handler_name, _get_root_handler, _remove_root_handler

logger = logging.getLogger(__name__)


def test_configure_console_logger():
    # TODO: Remove any existing handlers leftover from other tests

    ch = _remove_root_handler(_console_handler_name)
    fh = _remove_root_handler(_file_handler_name)

    templogfile = Path('./.tmpdir/log.txt').resolve()

    if not templogfile.parent.exists():
        os.makedirs(str(templogfile.parent), exist_ok=True)

    root_logger = dnaapp.logs.configure_root_logger()
    assert isinstance(_get_root_handler(_console_handler_name), logging.Handler)
    assert root_logger.level == logging.INFO
    assert not (_get_root_handler(_file_handler_name))

    with pytest.raises(NotADirectoryError):
        root_logger = dnaapp.logs.configure_root_logger(logfile='./doesnotexist/log.txt')
    root_logger = dnaapp.logs.configure_root_logger(logfile=templogfile)
    # assert root_logger.level == logging.INFO
    assert isinstance(_get_root_handler(_console_handler_name), logging.Handler)
    assert isinstance(_get_root_handler(_file_handler_name), logging.Handler)

    # Change logging level
    dnaapp.logs.set_logging_level(level=logging.DEBUG)
    assert root_logger.level == logging.DEBUG

    # os.remove(str(templogfile))
    # os.rmdir(str(templogfile.parent))
