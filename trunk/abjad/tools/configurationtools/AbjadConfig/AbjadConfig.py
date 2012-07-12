from abjad.tools import abctools
import collections
import os
import time


class AbjadConfig(collections.MutableMapping, abctools.AbjadObject):
    '''Abjad configuration object:

    ::

        >>> from abjad.tools.configurationtools import AbjadConfig
        >>> ABJCONFIG = AbjadConfig()
        >>> ABJCONFIG['accidental_spelling']
        'mixed'

    On instantiation, `AbjadConfig` creates the `$HOME/.abjad/` directory
    if it does not already exist.

    It then attempts to read an `abjad.cfg` file in that directory,
    parsing it as a `ConfigObj` configuration.  A default configuration
    is generated if no file is found.

    The `ConfigObj` instance is validated, and key:value pairs which
    fail validation are replaced by default values.

    The configuration is then written back to disk.

    Finally, the Abjad output directory is created if it does not already exist,
    by referencing the 'abjad_output' key in the configuration.

    `AbjadConfig` supports the mutable mapping interface, and can be subscripted as a dictionary.

    Returns `AbjadConfig` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_settings')

    ### INITIALIZER ###

    def __init__(self):

        import configobj
        import validate

        # verify configuration directory
        if not os.path.exists(self.ABJAD_CONFIG_DIRECTORY_PATH):
            os.mkdir(self.ABJAD_CONFIG_DIRECTORY_PATH)
        
        # attempt to load config from disk, and validate
        # a config object will be created if none is found on disk
        spec = self.get_config_spec()
        config = configobj.ConfigObj(self.ABJAD_CONFIG_FILE_PATH, configspec=spec)

        # validate
        validator = validate.Validator()
        validation = config.validate(validator, copy=True)

        # replace failing key:value pairs with default values
        if validation is not True:
            for key, valid in validation.iteritems():
                if not valid:
                    default = config.default_values[key]
                    print 'Warning: Abjad config key {!r} failed validation, '\
                        'setting to default: {!r}.'.format(key, default)
                    config[key] = default

        # setup output formatting
        config.write_empty_values = True
        config.comments.update(self.get_option_comments())
        config.initial_comment = self.get_initial_comment()

        # write back to disk
        with open(self.ABJAD_CONFIG_FILE_PATH, 'w') as f:
            config.write(f)

        # turn the ConfigObj instance into a standard dict,
        # and replace its empty string values with Nones,
        # caching the result on this AbjadConfig instance.
        self._settings = dict(config)
        for key, value in self._settings.iteritems():
            if value == '' or value == 'None':
                self._settings[key] = None

        # finally, verify the PDF output directory
        if not os.path.exists(self.ABJAD_OUTPUT_PATH):
            os.mkdir(self.ABJAD_OUTPUT_PATH)

    ### SPECIAL METHODS ###

    def __delitem__(self, i):
        del(self._settings[i])

    def __getitem__(self, i):
        return self._settings[i]

    def __iter__(self):
        for key in self._settings:
            yield key

    def __len__(self):
        return len(self._settings)

    def __setitem__(self, i, arg):
        self._settings[i] = arg

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def ABJAD_PATH(self):
        module_parts = self.__module__.split('.')
        filepath_parts = os.path.abspath(__file__).rpartition('.py')[0].split(os.path.sep)
        for part in reversed(module_parts):
            if part == 'abjad':
                break
            filepath_parts.pop()
        return os.path.sep.join(filepath_parts)

    @property
    def ABJAD_CONFIG_FILE_PATH(self):
        return os.path.join(self.ABJAD_CONFIG_DIRECTORY_PATH, 'abjad.cfg')

    @property
    def ABJAD_CONFIG_DIRECTORY_PATH(self):
        return os.path.join(self.HOME_PATH, '.abjad')

    @property
    def ABJAD_EXPERIMENTAL_PATH(self):
        return os.path.abspath(os.path.join(self.ABJAD_PATH, '..', '..', 'experimental'))

    @property
    def ABJAD_OUTPUT_PATH(self):
        return self._settings['abjad_output']

    @property
    def ABJAD_ROOT_PATH(self):
        return os.path.abspath(os.path.join(self.ABJAD_PATH, '..', '..'))

    @property
    def HOME_PATH(self):
        return os.environ.get('HOME') or os.environ.get('HOMEPATH') or os.environ.get('APPDATA')

    ### PUBLIC METHODS ###

    def get_config_spec(self):
        specs = self.get_option_specs()
        return ['{} = {}'.format(key, value) for key, value in sorted(specs.items())]

    def get_option_definitions(self):
        options = {
            'abjad_output': {
                'comment': [
                    '',
                    'Set to the one directory where you wish all Abjad generate files',
                    '(such as PDFs, LilyPond, MIDI or log files) to be saved.',
                    'Defaults to $HOME/.abjad/output/'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.ABJAD_CONFIG_DIRECTORY_PATH, 'output'))
            },
            'accidental_spelling': { 
                'comment': [
                    '',
                    'Default accidental spelling (mixed|sharps|flats).',
                ],
                'spec': "option('mixed', 'sharps', 'flats', default='mixed')"
            },
            'lilypond_includes': {
                'comment': [
                    '',
                    'Comma-separated list of LilyPond files that Abjad will "\include"',
                    'in all generated *.ly files',
                ],
                'spec': 'list(min=0, default=list())'
            },
            'lilypond_language': {
                'comment': [
                    '',
                    'Language to use in all generated LilyPond files.'
                ],
                'spec': "string(default='english')"
            },
            'lilypond_path': {
                'comment': [
                    '',
                    'Lilypond executable path.  Set to override dynamic lookup.'
                ],
                'spec': "string(default='lilypond')"
            },
            'midi_player': {
                'comment': [
                    '',
                    'MIDI player to play MIDI files with, via play().',
                    'When unset, your environment should know how to open MIDIs.',
                ],
                'spec': "string(default='')"
            },
            'pdf_viewer': {
                'comment': [
                    '',
                    'PDF viewer to view generated PDF files.',
                    'When unset, your environment should know how to open PDFs.',
                ],
                'spec': "string(default='')"
            },
            'text_editor': {
                'comment': [
                    '',
                    'Text editor for viewing text files with (i.e. *.ly).',
                    'When unset, your environment should know how to open text files.'
                ],
                'spec': "string(default='')"
            },

        }
        return options

    def get_option_comments(self):
        options = self.get_option_definitions()
        comments = [(key, options[key]['comment']) for key in options]
        return dict(comments)

    def get_option_specs(self):
        options = self.get_option_definitions()
        specs = [(key, options[key]['spec']) for key in options]
        return dict(specs)

    def get_initial_comment(self):
        return [
            '-*- coding: utf-8 -*-',
            ' ',
            'Abjad configuration file, created by Abjad on {}.'.format(time.strftime("%d %B %Y %H:%M:%S")),
            'This file is interpreted by ConfigObj, and should follow ini syntax.',
        ]

