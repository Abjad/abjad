# -*- encoding: utf-8 -*-
from __future__ import print_function
import abc
import configobj
import os
import time
import validate
from abjad.tools.abctools.AbjadObject import AbjadObject


class Configuration(AbjadObject):
    r'''A configuration object.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_settings',
        )

    ### INITIALIZER ###

    def __init__(self):
        from abjad.tools import systemtools
        # verify configuration directory
        if not os.path.exists(self.configuration_directory):
            os.makedirs(self.configuration_directory)
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
            for key, valid in validation.items():
                if not valid:
                    default = config.default_values[key]
                    message = 'Warning: config key {!r} failed validation,'
                    message += ' setting to default: {!r}.'
                    message = message.format(key, default)
                    print(message)
                    config[key] = default
        # setup output formatting
        config.write_empty_values = True
        config.comments.update(self._option_comments)
        config.initial_comment = self._initial_comment
        # write to disk if doesn't exist
        if not os.path.exists(self.configuration_file_path):
            if not os.path.exists(self.configuration_directory):
                os.makedirs(self.configuration_directory)
            config.write()
        # write to disk if different from current
        else:
            # prevent ConfigObj from automatically writing
            config.filename = None
            with open(self.configuration_file_path, 'r') as f:
                old_config_lines = f.read()

            old_config_lines = old_config_lines.splitlines()
            old_config_lines = [line for line in old_config_lines
                if 'configuration file created on' not in line]
            old_config_lines = '\n'.join(old_config_lines)
            new_config_lines = config.write(None)
            new_config_lines = [line for line in new_config_lines
                if 'configuration file created on' not in line]
            new_config_lines = '\n'.join(new_config_lines)

            lines_are_equal = systemtools.TestManager.compare(
                old_config_lines,
                new_config_lines,
                )
#            print('----------------------------------------')
#            print('TESTING:', type(self))
#            print()
#            print('OLD:')
#            print()
#            print(old_config_lines)
#            print()
#            print('NEW:')
#            print()
#            print(new_config_lines)
#            print()
#            print('EQUAL?', lines_are_equal)
#            print()
            if not lines_are_equal:
#                print('WRITING')
#                print()
                with open(self.configuration_file_path, 'w') as file_pointer:
                    config.write(file_pointer)
        # turn the ConfigObj instance into a standard dict,
        # and replace its empty string values with Nones,
        # caching the result on this AbjadConfiguration instance.
        self._settings = dict(config)
        for key, value in self._settings.items():
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

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _get_option_definitions(self):
        raise NotImplementedError

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
        options = self._get_option_definitions()
        comments = [(key, options[key]['comment']) for key in options]
        return dict(comments)

    @property
    def _option_specification(self):
        options = self._get_option_definitions()
        specs = [(key, options[key]['spec']) for key in options]
        return dict(specs)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def configuration_directory(self):
        r'''Gets configuration directory.

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
            self.configuration_directory,
            self.configuration_file_name,
            )

    @property
    def home_directory(self):
        r'''Gets home directory.

        Returns string.
        '''
        path = os.environ.get('HOME') or \
            os.environ.get('HOMEPATH') or \
            os.environ.get('APPDATA')
        return os.path.abspath(path)