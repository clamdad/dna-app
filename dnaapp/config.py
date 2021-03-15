# ------------------------------------------------------------------------------
# Copyright (c) 2021, Mike Babst
#
# Distributed under the terms of the MIT License
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
import json
import logging
from pathlib import Path

from atom.api import Atom, Enum, Typed

from dnaapp.base import Base, to_json_state, from_json_state

logger = logging.getLogger(__name__)


class ConfigOptions(Base):
    """ Config Options

    Each attribute represents an option in the config file.
    This object can be subclassed to add parameters.

    """
    loglevel = Enum('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')


class AppConfig(Atom):
    """
    
    """

    #: Container for config options
    options = property(lambda self: self._options)
    _options = Typed(ConfigOptions)

    #: Config file
    config_file = property(lambda self: self._config_file)
    _config_file = Typed(Path)

    def __init__(self, config_file=None, **kwargs):

        super(AppConfig).__init__(**kwargs)

        if config_file:
            self._config_file = Path(config_file).resolve().absolute()

        self.load()

    def load(self):

        if self.config_file:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    try:
                        state = json.load(f)
                        obj = from_json_state(state)
                        self._options = obj
                        return
                    except json.JSONDecodeError:
                        logger.error('Error decoding JSON configuration file: {}'.format(self.config_file))

            else:
                logger.warning('Config file does not exist: {}'.format(self.config_file))

        logger.warning('Loading default configuration')
        cfg = ConfigOptions()
        logger.debug('Loading configuration {}'.format(cfg))
        self._options = cfg

    def save(self):

        try:
            with open(self.config_file, 'w') as f:
                state = to_json_state(self.options, references=False)
                json.dump(state, f, indent=2)
            logger.info('Saved configuration to {}'.format(self.config_file))
        except FileNotFoundError as e:
            logger.error('Error writing config file {}'.format(self.config_file))
            raise (e)