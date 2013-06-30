import os
from abjad.tools.configurationtools.Configuration import Configuration


class AbjadConfiguration(Configuration):
    '''Abjad configuration object:

    ::

        >>> ABJCONFIG = configurationtools.AbjadConfiguration()
        >>> ABJCONFIG['accidental_spelling']
        'mixed'

    `AbjadConfiguration` creates the `$home/.abjad/` directory 
    on instantiation.

    `AbjadConfiguration` then attempts to read an `abjad.cfg` file in 
    that directory and parse the file as a `ConfigObj` configuration.
    `AbjadConfiguration` generates a default configuration if no file 
    is found.

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
        if not os.path.exists(self.abjad_output_directory_path):
            os.mkdir(self.abjad_output_directory_path)

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
            # TODO: change name to 'abjad_output_directory_path'
            'abjad_output': {
                'comment': [
                    '',
                    'Set to the one directory where you wish all Abjad-generated files',
                    '(such as PDFs, LilyPond, MIDI or log files) to be saved.',
                    'Defaults to $home/.abjad/output/'
                ],
                'spec': 'string(default={!r})'.format(
                    os.path.join(
                        self.abjad_configuration_directory_path, 'output'))
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

    ### PUBLIC PROPERTIES ###

    @property
    def abjad_configuration_directory_path(self):
        return os.path.join(self.home_directory_path, '.abjad')

    @property
    def abjad_configuration_file_path(self):
        return self.configuration_file_path

    @property
    def abjad_directory_path(self):
        module_parts = self.__module__.split('.')
        filepath_parts = os.path.abspath(__file__).rpartition('.py')
        filepath_parts = filepath_parts[0].split(os.path.sep)
        for part in reversed(module_parts):
            if part == 'abjad':
                break
            filepath_parts.pop()
        return os.path.sep.join(filepath_parts)

    @property
    def abjad_experimental_directory_path(self):
        return os.path.abspath(os.path.join(
            self.abjad_directory_path, '..', '..', 'experimental'))

    @property
    def abjad_output_directory_path(self):
        return self._settings['abjad_output']

    @property
    def abjad_root_directory_path(self):
        return os.path.abspath(os.path.join(
            self.abjad_directory_path, '..', '..'))

    @property
    def configuration_directory_path(self):
        return self.abjad_configuration_directory_path

    @property
    def configuration_file_name(self):
        return 'abjad.cfg'
