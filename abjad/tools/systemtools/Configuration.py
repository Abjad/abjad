# -*- encoding: utf-8 -*-
from __future__ import print_function
from abjad.tools.abctools.AbjadObject import AbjadObject
from six.moves import StringIO
from six.moves import configparser
import abc
import os
import six
import time


class Configuration(AbjadObject):
    r'''A configuration object.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'System configuration'

    __slots__ = (
        '_settings',
        )

    ### INITIALIZER ###

    def __init__(self):
        if not os.path.exists(self.configuration_directory):
            os.makedirs(self.configuration_directory)
        old_contents = ''
        if os.path.exists(self.configuration_file_path):
            with open(self.configuration_file_path, 'r') as file_pointer:
                old_contents = file_pointer.read()
        configuration = self._configuration_from_string(old_contents)
        configuration = self._validate_configuration(configuration)
        new_contents = self._configuration_to_string(configuration)
        if not self._compare_configurations(old_contents, new_contents):
            with open(self.configuration_file_path, 'w') as file_pointer:
                file_pointer.write(new_contents)
        self._settings = configuration

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

    def _compare_configurations(self, old, new):
        old = '\n'.join(old.splitlines()[3:])
        new = '\n'.join(new.splitlines()[3:])
        return old == new

    def _configuration_from_string(self, string):
        if '[main]' not in string:
            string = '[main]\n' + string
        config_parser = configparser.ConfigParser()
        try:
            if six.PY3:
                config_parser.read_string(string)
                configuration = dict(config_parser['main'].items())
            else:
                string_io = StringIO(string)
                config_parser.readfp(string_io)
                configuration = dict(config_parser.items('main'))
        except configparser.ParsingError:
            configuration = {}
        return configuration

    def _configuration_to_string(self, configuration):
        option_definitions = self._get_option_definitions()
        known_items, unknown_items = [], []
        for key, value in sorted(configuration.items()):
            if key in option_definitions:
                known_items.append((key, value))
            else:
                unknown_items.append((key, value))
        result = []
        for line in self._initial_comment:
            if line:
                result.append('# {}'.format(line))
            else:
                result.append('')
        for key, value in known_items:
            result.append('')
            if key in option_definitions:
                for line in option_definitions[key]['comment']:
                    if line:
                        result.append('# {}'.format(line))
                    else:
                        result.append('')
            if value not in ('', None):
                result.append('{!s} = {!s}'.format(key, value))
            else:
                result.append('{!s} ='.format(key))
        if unknown_items:
            result.append('')
            result.append('# User-specified keys:')
            for key, value in unknown_items:
                result.append('')
                if value not in ('', None):
                    result.append('{!s} = {!s}'.format(key, value))
                else:
                    result.append('{!s} ='.format(key))
        string = '\n'.join(result)
        return string

    @abc.abstractmethod
    def _get_option_definitions(self):
        raise NotImplementedError

    def _validate_configuration(self, configuration):
        option_definitions = self._get_option_definitions()
        for key in option_definitions:
            if key not in configuration:
                configuration[key] = option_definitions[key]['default']
            validator = option_definitions[key]['validator']
            if isinstance(validator, type):
                if not isinstance(configuration[key], validator):
                    configuration[key] = option_definitions[key]['default']
            else:
                if not validator(configuration[key]):
                    configuration[key] = option_definitions[key]['default']
        for key in configuration:
            if configuration[key] in ('', 'None'):
                configuration[key] = None
        return configuration

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
        path = (
            os.environ.get('HOME') or
            os.environ.get('HOMEPATH') or
            os.environ.get('APPDATA')
            )
        return os.path.abspath(path)