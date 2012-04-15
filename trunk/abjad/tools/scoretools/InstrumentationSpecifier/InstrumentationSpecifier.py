from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.scoretools.PerformerInventory import PerformerInventory


class InstrumentationSpecifier(AbjadObject):
    r'''.. versionadded:: 2.5

    Abjad model of score instrumentation::

        abjad> flute = scoretools.Performer('Flute')
        abjad> flute.instruments.append(instrumenttools.Flute())
        abjad> flute.instruments.append(instrumenttools.AltoFlute())

    ::

        abjad> guitar = scoretools.Performer('Guitar')
        abjad> guitar.instruments.append(instrumenttools.Guitar())

    ::

        abjad> instrumentation_specifier = scoretools.InstrumentationSpecifier([flute, guitar])

    ::

        abjad> instrumentation_specifier
        InstrumentationSpecifier(performers=PerformerInventory([Performer(name='Flute', instruments=InstrumentInventory([Flute(), AltoFlute()])), Performer(name='Guitar', instruments=InstrumentInventory([Guitar()]))]))

    Return instrumentation specifier.
    '''

    def __init__(self, performers=None):
        self._performers = PerformerInventory()
        self.performers = performers

    ### SPECIAL METHODS ###
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            # TODO: implement perform sort
            #if sorted(self.performers) == sorted(other.performers):
            if self.performers == other.performers:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    ### PUBLIC PROPERTIES ###

    @property
    def instrument_count(self):
        r'''Read-only number of instruments in score::
    
            abjad> instrumentation_specifier.instrument_count
            3

        Return nonnegative integer.
        '''
        return len(self.instruments)

    @property
    def instruments(self):
        r'''Read-only list of instruments derived from performers::

            abjad> instrumentation_specifier.instruments
            [Flute(), AltoFlute(), Guitar()]

        Return list.
        '''        
        instruments = []
        for performer in self.performers:
            instruments.extend(performer.instruments)
        return instruments

    @property
    def performer_count(self):
        r'''Read-only number of performers in score::

            abjad> instrumentation_specifier.performer_count
            2

        Return nonnegative integer.
        '''
        return len(self.performers)

    @property
    def performer_name_string(self):
        r'''Read-only string of performer names::

            abjad> instrumentation_specifier.performer_name_string
            'Flute, Guitar'

        Return string.
        '''
        if self.performers:
            return ', '.join([performer.name for performer in self.performers])
        else:
            return ''

    @apply
    def performers():
        def fget(self):
            r'''Read / write list of performers in score::

                abjad> instrumentation_specifier.performers
                PerformerInventory([Performer(name='Flute', instruments=InstrumentInventory([Flute(), AltoFlute()])), Performer(name='Guitar', instruments=InstrumentInventory([Guitar()]))])

            Return list.
            '''
            return self._performers
        def fset(self, performers):
            from abjad.tools import scoretools
            assert isinstance(performers, (list, type(None)))
            if performers is None:
                self._performers[:] = []
            else:
                assert all([isinstance(x, scoretools.Performer) for x in performers])
                self._performers[:] = list(performers[:])
        return property(**locals())
