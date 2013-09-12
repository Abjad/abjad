# -*- encoding: utf-8 -*-
import abc
import configobj
import os
import time
import validate
from abjad.tools import abctools


class Configuration(abctools.AbjadObject):
    r'''A configuration object.
    '''

    ### INITIALIZER ###

    def __init__(self):
        # verify configuration directory
        if not os.path.exists(self.configuration_directory_path):
            os.makedirs(self.configuration_directory_path)
        # attempt to load config from disk, and validate
        # a config object will be created if none is found on disk
        config = configobj.ConfigObj(
            self.configuration_file_path,
            configspec=self._config_specification
            )
        # validate
        validator = validate.Validator()
        validation = config.validate(validator, copy=True)
        # replace failing key:value pairs with default values
        if validation is not True:
            for key, valid in validation.iteritems():
                if not valid:
                    default = config.default_values[key]
                    message = 'Warning: config key {!r} failed validation,'
                    message += ' setting to default: {!r}.'
                    message = message.format(key, default)
                    print message
                    config[key] = default
        # setup output formatting
        config.write_empty_values = True
        config.comments.update(self._option_comments)
        config.initial_comment = self._initial_comment
        # write back to disk
        with open(self.configuration_file_path, 'w') as f:
            config.write(f)
        # turn the ConfigObj instance into a standard dict,
        # and replace its empty string values with Nones,
        # caching the result on this AbjadConfiguration instance.
        self._settings = dict(config)
        for key, value in self._settings.iteritems():
            if value == '' or value == 'None':
                self._settings[key] = None

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        r'''Deletes `i` from settings.

        Returns none.
        '''
        del(self._settings[i])

    def __getitem__(self, i):
        r'''Gets `i` from settings.

        Returns none.
        '''
        return self._settings[i]

    def __iter__(self):
        r'''Iterates settings.

        Returns generator.
        '''
        for key in self._settings:
            yield key

    def __len__(self):
        r'''Number of settings in configuration.

        Returns nonnegative integer.
        '''
        return len(self._settings)

    def __setitem__(self, i, arg):
        r'''Sets setting `i` to `arg`.

        Returns none.
        '''
        self._settings[i] = arg

    ### PRIVATE PROPERTIES ###

    @property
    def _config_specification(self):
        specs = self._option_specification
        return ['{} = {}'.format(key, value) 
            for key, value in sorted(specs.items())]

    @property
    def _current_time(self):
        return time.strftime("%d %B %Y %H:%M:%S")

    @abc.abstractproperty
    def _initial_comment(self):
        raise NotImplemented

    @property
    def _option_comments(self):
        options = self._option_definitions
        comments = [(key, options[key]['comment']) for key in options]
        return dict(comments)

    @abc.abstractproperty
    def _option_definitions(self):
        raise NotImplemented

    @property
    def _option_specification(self):
        options = self._option_definitions
        specs = [(key, options[key]['spec']) for key in options]
        return dict(specs)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def configuration_directory_path(self):
        r'''Configuration directory path.

        Returns string.
        '''
        raise NotImplemented

    @abc.abstractproperty
    def configuration_file_name(self):
        r'''Configuration file name.

        Returns string.
        '''
        raise NotImplemented

    @property
    def configuration_file_path(self):
        r'''Configuration file path.

        Returns string.
        '''
        return os.path.join(
            self.configuration_directory_path, 
            self.configuration_file_name,
            )

    @property
    def home_directory_path(self):
        r'''Home directory path.

        Returns string.
        '''
        return os.environ.get('HOME') or \
            os.environ.get('HOMEPATH') or \
            os.environ.get('APPDATA')
