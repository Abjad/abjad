import os
from abjad.tools.configurationtools.Configuration import Configuration


class AbjadConfig(Configuration):
    '''Abjad configuration object:

    ::

        >>> ABJCONFIG = configurationtools.AbjadConfig()
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

    ### INITIALIZER ###

    def __init__(self):

        Configuration.__init__(self)

        # verify the PDF output directory
        if not os.path.exists(self.ABJAD_OUTPUT_PATH):
            os.mkdir(self.ABJAD_OUTPUT_PATH)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def ABJAD_CONFIG_DIRECTORY_PATH(self):
        return os.path.join(self.HOME_DIRECTORY_PATH, '.abjad')

    @property
    def ABJAD_CONFIG_FILE_PATH(self):
        return self.CONFIG_FILE_PATH

    @property
    def ABJAD_EXPERIMENTAL_PATH(self):
        return os.path.abspath(os.path.join(self.ABJAD_PATH, '..', '..', 'experimental'))

    @property
    def ABJAD_OUTPUT_PATH(self):
        return self._settings['abjad_output']

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
    def ABJAD_ROOT_PATH(self):
        return os.path.abspath(os.path.join(self.ABJAD_PATH, '..', '..'))

    @property
    def CONFIG_DIRECTORY_PATH(self):
        return self.ABJAD_CONFIG_DIRECTORY_PATH

    @property
    def CONFIG_FILE_NAME(self):
        return 'abjad.cfg'

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return [
            '-*- coding: utf-8 -*-',
            ' ',
            'Abjad configuration file, created by Abjad on {}.'.format(
                self._current_time),
            'This file is interpreted by ConfigObj, and should follow ini syntax.',
        ]

    @property
    def _option_definitions(self):
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

