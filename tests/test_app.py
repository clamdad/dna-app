# ------------------------------------------------------------------------------
# Copyright (c) 2021, Mike Babst
#
# Distributed under the terms of the MIT License
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

import os

import pytest
from dnaapp import default_appname
from dnaapp.app import AppModel


def test_app_constructor():
    # Create an application
    app = AppModel(default_appname)

    # Prevent creating two Applications
    with pytest.raises(RuntimeError):
        app = AppModel(default_appname)

    # Destroy existing app
    app.destroy()

    # Create a new app using local home folder
    os.mkdir('.tmp')
    app = AppModel(default_appname, home='.tmp')
    app.destroy()

    # Try to use non-existent directory
    with pytest.raises(NotADirectoryError):
        os.rmdir('.tmp')
        app = AppModel(default_appname, home='.tmp')

    # Test app getter (create from scratch)
    app.destroy()
    app1 = AppModel(default_appname).get()

    # Re-get existing app object
    app2 = AppModel.get()

    assert app1 is app2

    app2.config.save()
