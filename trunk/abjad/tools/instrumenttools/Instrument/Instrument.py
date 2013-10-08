# -*- encoding: utf-8 -*-
import abc
import inspect
from abjad.tools import contexttools
from abjad.tools import pitchtools


class Instrument(contexttools.InstrumentMark):
    '''A musical instrument.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        instrument_name=None,
        short_instrument_name=None,
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        target_context=None,
        ):
        self._sounding_pitch_of_written_middle_c = pitchtools.NamedPitch("c'")
        contexttools.InstrumentMark.__init__(
            self,
            instrument_name,
            short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            target_context=target_context,
            )
        self._default_performer_names = ['instrumentalist']
        self._is_primary_instrument = False
        self._pitch_range = None

    ### PRIVATE METHODS ###

    def _copy_starting_clefs_to_allowable_clefs(self):
        inventory = contexttools.ClefMarkInventory(self.starting_clefs)
        self.allowable_clefs = inventory

    def _get_default_performer_name(self):
        if self._default_performer_names is None:
            performer_name = '{} player'.format(self._default_instrument_name)
            return performer_name
        else:
            return self._default_performer_names[-1]

    def _get_performer_names(self):
        if self._default_performer_names is None:
            performer_name = '{} player'.format(self._default_instrument_name)
            return [performer_name]
        else:
            return self._default_performer_names[:]

    @classmethod
    def _list_instrument_names(cls):
        r'''Lists instrument names.

        ::

            >>> function = instrumenttools.Instrument._list_instrument_names
            >>> for instrument_name in function():
            ...     instrument_name
            ...
            'accordion'
            'alto flute'
            'alto saxophone'
            'alto trombone'
            'baritone saxophone'
            'baritone voice'
            'bass clarinet'
            'bass flute'
            'bass saxophone'
            'bass trombone'
            'bass voice'
            'bassoon'
            'cello'
            ...

        Returns list.
        '''
        instrument_names = []
        for instrument_class in cls._list_instruments():
            instrument = instrument_class()
            instrument_names.append(instrument.instrument_name)
        instrument_names.sort(key=lambda x: x.lower())
        return instrument_names

    @staticmethod
    def _list_instruments(classes=None):
        r'''Lists instruments.

        ::

            >>> function = instrumenttools.Instrument._list_instruments
            >>> for instrument in function():
            ...     instrument.__name__
            ...
            'Accordion'
            'AltoFlute'
            'AltoSaxophone'
            'AltoTrombone'
            'BaritoneSaxophone'
            ...

        Returns list.
        '''
        from abjad.tools import instrumenttools
        if classes is None:
            classes = (instrumenttools.Instrument,)
        instruments = []
        for value in instrumenttools.__dict__.itervalues():
            try:
                if issubclass(value, classes) \
                    and not inspect.isabstract(value):
                    instruments.append(value)
            except TypeError:
                pass
        instruments.sort(key=lambda x: x.__name__.lower())
        return instruments

    @classmethod
    def _list_primary_instruments(cls):
        primary_instruments = []
        for instrument_class in cls._list_instruments():
            instrument = instrument_class()
            if instrument._is_primary_instrument:
                primary_instruments.append(instrument_class)
        return primary_instruments

    @classmethod
    def _list_secondary_instruments(cls):
        secondary_instruments = []
        for instrument_class in cls._list_instruments():
            instrument = instrument_class()
            if not instrument._is_primary_instrument:
                secondary_instruments.append(instrument_class)
        return secondary_instruments

    ### PUBLIC PROPERTIES ###

    @apply
    def allowable_clefs():
        def fget(self):
            r'''Gets and sets allowable clefs.

            Returns clef inventory.
            '''
            return self._allowable_clefs
        def fset(self, clefs):
            self._allowable_clefs = contexttools.ClefMarkInventory(clefs)
        return property(**locals())

    @apply
    def pitch_range():
        def fget(self):
            r'''Gets and sets pitch range.

            Returns pitch range.
            '''
            if self._pitch_range is None:
                return self._default_pitch_range
            return self._pitch_range
        def fset(self, pitch_range):
            if pitch_range is not None:
                pitch_range = pitchtools.PitchRange(pitch_range)
            self._pitch_range = pitch_range
        return property(**locals())

    @apply
    def starting_clefs():
        def fget(self):
            r'''Gets and sets starting clefs.

            Returns clef inventory.
            '''
            return self._starting_clefs
        def fset(self, clefs):
            self._starting_clefs = contexttools.ClefMarkInventory(clefs)
        return property(**locals())

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            Returns named pitch.
            '''
            return self._sounding_pitch_of_written_middle_c
        def fset(self, pitch):
            pitch = pitchtools.NamedPitch(pitch)
            self._sounding_pitch_of_written_middle_c = pitch
        return property(**locals())
