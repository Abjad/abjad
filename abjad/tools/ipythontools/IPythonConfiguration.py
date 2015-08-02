# -*- encoding: utf-8 -*-
import os
from abjad.tools.systemtools.Configuration import Configuration


class IPythonConfiguration(Configuration):
    r'''Abjad IPython extension configuration.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        Configuration.__init__(self)

    ### PRIVATE METHODS ###

    def _get_option_definitions(self):
        options = {
            'midi_bank': {
                'comment': ['Sound font MIDI bank.'],
                'default': 'gs',
                'validator': str,
                },
            'sound_font': {
                'comment': ['Sound font file path.'],
                'default': '',
                'validator': str,
                },
            }
        return options

    ### PRIVATE PROPERTIES ###

    @property
    def _initial_comment(self):
        current_time = self._current_time
        return [
            '-*- coding: utf-8 -*-',
            '',
            'IPython configuration file created on {}.'.format(current_time),
            "This file is interpreted by Python's ConfigParser ",
            'and follows ini sytnax.',
            ]

    ### PUBLIC METHODS ###

    @property
    def configuration_directory(self):
        r'''Configuration directory.

        Returns string.
        '''
        import abjad
        return os.path.join(
            abjad.abjad_configuration.abjad_configuration_directory,
            'ipython',
            )

    @property
    def configuration_file_name(self):
        r'''Configuration file name.

        Returns string.
        '''
        return 'ipython.cfg'