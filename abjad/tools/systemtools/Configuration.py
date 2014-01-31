# -*- encoding: utf-8 -*-
import abc
import configobj
import os
import time
import validate
from abjad.tools.abctools.AbjadObject import AbjadObject


class Configuration(AbjadObject):
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
        # write to disk if doesn't exist
        if not os.path.exists(self.configuration_file_path):
            if not os.path.exists(self.configuration_directory_path):
                os.makedirs(self.configuration_directory_path)
            config.write()
        # write to disk if different from current
        else:
            # prevent ConfigObj from automatically writing
            config.filename = None
            with open(self.configuration_file_path, 'r') as f:
                old_config_lines = f.read().splitlines()
            while len(old_config_lines) and (
                old_config_lines[0].startswith('#') or
                not old_config_lines[0].strip()):
                old_config_lines.pop(0)
            new_config_lines = config.write(None)
            while len(new_config_lines) and (
                new_config_lines[0].startswith('#') or
                not new_config_lines[0].strip()):
                new_config_lines.pop(0)
            if old_config_lines != new_config_lines:
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
        r'''Deletes item `i` from configuration.

        Returns none.
        '''
        del(self._settings[i])

    def __getitem__(self, i):
        r'''Gets item `i` from configuration.

        Returns none.
        '''
        return self._settings[i]

    def __iter__(self):
        r'''Iterates configuration settings.

        Returns generator.
        '''
        for key in self._settings:
            yield key

    def __len__(self):
        r'''Gets the number of settings in configuration.

        Returns nonnegative integer.
        '''
        return len(self._settings)

    def __setitem__(self, i, arg):
        r'''Sets configuration item `i` to `arg`.

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
        raise NotImplementedError

    @property
    def _option_comments(self):
        options = self._option_definitions
        comments = [(key, options[key]['comment']) for key in options]
        return dict(comments)

    @abc.abstractproperty
    def _option_definitions(self):
        raise NotImplementedError

    @property
    def _option_specification(self):
        options = self._option_definitions
        specs = [(key, options[key]['spec']) for key in options]
        return dict(specs)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def configuration_directory_path(self):
        r'''Gets configuration directory path.

        Returns string.
        '''
        raise NotImplementedError

    @abc.abstractproperty
    def configuration_file_name(self):
        r'''Gets configuration file name.

        Returns string.
        '''
        raise NotImplementedError

    @property
    def configuration_file_path(self):
        r'''Gets configuration file path.

        Returns string.
        '''
        return os.path.join(
            self.configuration_directory_path,
            self.configuration_file_name,
            )

    @property
    def home_directory_path(self):
        r'''Gets home directory path.

        Returns string.
        '''
        path = os.environ.get('HOME') or \
            os.environ.get('HOMEPATH') or \
            os.environ.get('APPDATA')
        return os.path.abspath(path)
