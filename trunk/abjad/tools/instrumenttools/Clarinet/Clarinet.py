import abc
from abjad.tools.instrumenttools.SingleReedInstrument import SingleReedInstrument


class Clarinet(SingleReedInstrument):
    r'''.. versionadded:: 2.6

    Abjad model of the family of clarinets.
    '''

    ### INITIALIZER ###
    
    @abc.abstractmethod
    def __init__(self, **kwargs):
        SingleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'clarinet'
        self._default_performer_names.extend(['clarinettist', 'clarinetist'])
        self._default_short_instrument_name = 'cl.'
