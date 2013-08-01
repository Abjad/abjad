# -*- encoding: utf-8 -*-
import abc
from abjad.tools.instrumenttools.BrassInstrument import BrassInstrument


class Trombone(BrassInstrument):
    r'''Abjad model of the family of trombones.
    '''

    ### CLASS VARIABLES ###

    default_performer_abbreviation = 'trb.'

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        BrassInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'trombone'
        self._default_performer_names.append('trombonist')
        self._default_short_instrument_name = 'trb.'
