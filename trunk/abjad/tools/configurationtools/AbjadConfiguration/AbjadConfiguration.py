import os
from abjad.tools.configurationtools.Configuration import Configuration


class AbjadConfiguration(Configuration):
    '''Abjad configuration object:

    ::

        >>> ABJCONFIG = configurationtools.AbjadConfiguration()
        >>> ABJCONFIG['accidental_spelling']
        'mixed'

    `AbjadConfiguration` creates the `$HOME/.abjad/` directory on instantiation.

    `AbjadConfiguration` then attempts to read an `abjad.cfg` file in that directory
    and parse the file as a `ConfigObj` configuration.
    `AbjadConfiguration` generates a default configuration if no file is found.

    `AbjadConfiguration` validates the `ConfigObj` instance
    and replaces key-value pairs which fail validation with default values.
    `AbjadConfiguration` then writes the configuration back to disk.

    The Abjad output directory is created the from `abjad_output` key
    if it does not already exist.

    `AbjadConfiguration` supports the mutable mapping interface 
    and can be subscripted as a dictionary.
    '''

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)
        # verify the PDF output directory
        if not os.path.exists(self.ABJAD_OUTPUT_PATH):
            os.mkdir(self.ABJAD_OUTPUT_PATH)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        return [
            '-*- coding: utf-8 -*-',
            '',
            'Abjad configuration file created by Abjad on {}.'.format(
                self._current_time),
            'This file is interpreted by ConfigObj and should follow ini syntax.',
        ]

    @property
    def _option_definitions(self):
        options = {
            # TODO: should this be renamed to 'abjad_output_directory_path'?
            'abjad_output': {
                'comment': [
                    '',
                    'Set to the one directory where you wish all Abjad-generated files',
                    '(such as PDFs, LilyPond, MIDI or log files) to be saved.',
                    'Defaults to $HOME/.abjad/output/'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(self.ABJAD_CONFIGURATION_DIRECTORY_PATH, 'output'))
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
                    'Lilypond executable path. Set to override dynamic lookup.'
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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def ABJAD_CONFIGURATION_DIRECTORY_PATH(self):
        return os.path.join(self.HOME_DIRECTORY_PATH, '.abjad')

    @property
    def ABJAD_CONFIGURATION_FILE_PATH(self):
        return self.CONFIGURATION_FILE_PATH

    # TODO: change name to ABJAD_EXPERIMENTAL_DIRECTORY_PATH
    @property
    def ABJAD_EXPERIMENTAL_PATH(self):
        return os.path.abspath(os.path.join(self.ABJAD_PATH, '..', '..', 'experimental'))

    # TODO: change name to ABJAD_OUTPUT_DIRECTORY_PATH
    @property
    def ABJAD_OUTPUT_PATH(self):
        return self._settings['abjad_output']

    # TODO: change name to ABJAD_DIRECTORY_PATH
    @property
    def ABJAD_PATH(self):
        module_parts = self.__module__.split('.')
        filepath_parts = os.path.abspath(__file__).rpartition('.py')[0].split(os.path.sep)
        for part in reversed(module_parts):
            if part == 'abjad':
                break
            filepath_parts.pop()
        return os.path.sep.join(filepath_parts)

    # TODO: change name to ABJAD_ROOT_DIRECTORY_PATH
    @property
    def ABJAD_ROOT_PATH(self):
        return os.path.abspath(os.path.join(self.ABJAD_PATH, '..', '..'))

    @property
    def CONFIGURATION_DIRECTORY_PATH(self):
        return self.ABJAD_CONFIGURATION_DIRECTORY_PATH

    @property
    def CONFIGURATION_FILE_NAME(self):
        return 'abjad.cfg'
