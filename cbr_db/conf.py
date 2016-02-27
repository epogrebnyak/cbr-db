"""
This module contains global ``settings`` object.

Settings object can be accessed using ``from .conf import settings``.

You can override settings module with CBR_DB_SETTINGS variable.
"""
import os


class _SettingsWrapper(object):

    def __init__(self):
        self._settings = None

    def __getattr__(self, name):
        if self._settings is None:
            if os.environ.get('CBR_DB_SETTINGS'):
                load_settings(os.environ['CBR_DB_SETTINGS'])
            else:
                raise Exception('settings are not loaded')
        return getattr(self._settings, name)


settings = _SettingsWrapper()


def load_settings(settings_module=None):
    """
    Any executable script must call this method before using settings.
    """
    import importlib
    global settings
    if settings_module is None:
        settings_module = os.environ['CBR_DB_SETTINGS']
    settings._settings = importlib.import_module(settings_module)
