# -*- encoding: utf-8 -*-
import abc
from abjad.tools.instrumenttools.SingleReedInstrument \
    import SingleReedInstrument


class Saxophone(SingleReedInstrument):
    r'''Abjad model of the family of saxophones.
    '''

    ### CLASS VARIABLES ###

    # TODO: remove?
    default_perfomer_abbreviation = 'sax.'

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        SingleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'sax.'
