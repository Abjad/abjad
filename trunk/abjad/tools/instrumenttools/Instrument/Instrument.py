# -*- encoding: utf-8 -*-
import abc
import inspect
from abjad.tools import contexttools
from abjad.tools import pitchtools


class Instrument(contexttools.InstrumentMark):
    '''Abjad model of the musical instrument.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self,
        instrument_name=None,
        short_instrument_name=None,
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        target_context=None,
        ):
        self.sounding_pitch_of_written_middle_c = \
            pitchtools.NamedChromaticPitch("c'")
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

    def _copy_primary_clefs_to_all_clefs(self):
        self.all_clefs = contexttools.ClefMarkInventory(self.primary_clefs)

    ### PUBLIC PROPERTIES ###

    @apply
    def all_clefs():
        def fset(self, clefs):
            r'''Read / write all clefs.

            Return tuple of clefs.
            '''
            self._all_clefs = contexttools.ClefMarkInventory(clefs)
        def fget(self):
            return self._all_clefs
        return property(**locals())

    @property
    def default_pitch_range(self):
        r'''Traditional pitch range.

        Return pitch range.
        '''
        return self._traditional_pitch_range

    @property
    def interval_of_transposition(self):
        r'''Interval of transposition.

        Return melodic diatonic interval.
        '''
        return pitchtools.NamedChromaticPitch("c'") - \
            self.sounding_pitch_of_written_middle_c

    @property
    def is_primary_instrument(self):
        return self._is_primary_instrument

    @property
    def is_secondary_instrument(self):
        return not self.is_primary_instrument

    @property
    def is_transposing(self):
        r'''True when instrument is transposing. False otherwise.

        Return boolean.
        '''
        return not self.sounding_pitch_of_written_middle_c == \
            pitchtools.NamedChromaticPitch("c'")

    @apply
    def pitch_range():
        def fset(self, pitch_range):
            r'''Read / write pitch range.

            Return pitch range.
            '''
            if pitch_range is not None:
                pitch_range = pitchtools.PitchRange(pitch_range)
            self._pitch_range = pitch_range
        def fget(self):
            if self._pitch_range is None:
                return self.default_pitch_range
            return self._pitch_range
        return property(**locals())

    @apply
    def primary_clefs():
        def fset(self, clefs):
            r'''Read / write primary clefs.

            Return tuple of clefs.
            '''
            self._primary_clefs = contexttools.ClefMarkInventory(clefs)
        def fget(self):
            return self._primary_clefs
        return property(**locals())

    @apply
    def sounding_pitch_of_written_middle_c():
        def fset(self, pitch):
            r'''Read / write sounding pitch of written middle C.

            Return named chromatic pitch.
            '''
            pitch = pitchtools.NamedChromaticPitch(pitch)
            self._sounding_pitch_of_written_middle_c = pitch
        def fget(self):
            return self._sounding_pitch_of_written_middle_c
        return property(**locals())

    ### PUBLIC METHODS ###

    def get_default_performer_name(self):
        r'''Get default player name.
        '''
        if self._default_performer_names is None:
            performer_name = '{} player'.format(self.default_instrument_name)
            return performer_name
        else:
            return self._default_performer_names[-1]

    def get_performer_names(self):
        r'''Get performer names.
        '''
        if self._default_performer_names is None:
            performer_name = '{} player'.format(self.default_instrument_name)
            return [performer_name]
        else:
            return self._default_performer_names[:]

    @classmethod
    def list_instrument_names(cls):
        r'''List instrument names:

        ::

            >>> for instrument_name in instrumenttools.Instrument.\
            ...     list_instrument_names():
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
            'clarinet in A'
            'clarinet in B-flat'
            'clarinet in E-flat'
            'contrabass'
            'contrabass clarinet'
            'contrabass flute'
            'contrabass saxophone'
            'contrabassoon'
            'contralto voice'
            'English horn'
            'flute'
            'glockenspiel'
            'guitar'
            'harp'
            'harpsichord'
            'horn'
            'marimba'
            'mezzo-soprano voice'
            'oboe'
            'piano'
            'piccolo'
            'sopranino saxophone'
            'soprano saxophone'
            'soprano voice'
            'tenor saxophone'
            'tenor trombone'
            'tenor voice'
            'trumpet'
            'tuba'
            'untuned percussion'
            'vibraphone'
            'viola'
            'violin'
            'xylophone'

        Return list.
        '''
        instrument_names = []
        for instrument_class in cls.list_instruments():
            instrument = instrument_class()
            instrument_names.append(instrument.instrument_name)
        instrument_names.sort(key=lambda x: x.lower())
        return instrument_names

    @staticmethod
    def list_instruments(classes=None):
        r'''List instruments in ``instrumenttools`` module:

        ::

            >>> for instrument in instrumenttools.Instrument.\
            ...     list_instruments()[:5]:
            ...     instrument.__name__
            ...
            'Accordion'
            'AltoFlute'
            'AltoSaxophone'
            'AltoTrombone'
            'BaritoneSaxophone'

        Return list.
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
    def list_primary_instruments(cls):
        r'''List primary instruments:

        ::

            >>> for instrument in instrumenttools.Instrument.\
            ...     list_primary_instruments():
            ...     instrument.__name__
            ...
            'Accordion'
            'AltoSaxophone'
            'BaritoneVoice'
            'Bassoon'
            'BassVoice'
            'BFlatClarinet'
            'Cello'
            'Contrabass'
            'ContraltoVoice'
            'Flute'
            'FrenchHorn'
            'Guitar'
            'Harp'
            'Harpsichord'
            'MezzoSopranoVoice'
            'Oboe'
            'Piano'
            'SopranoVoice'
            'TenorTrombone'
            'TenorVoice'
            'Trumpet'
            'Tuba'
            'Viola'
            'Violin'

        Return list
        '''
        primary_instruments = []
        for instrument_class in cls.list_instruments():
            instrument = instrument_class()
            if instrument.is_primary_instrument:
                primary_instruments.append(instrument_class)
        return primary_instruments

    @classmethod
    def list_secondary_instruments(cls):
        r'''List secondary instruments:

        ::

            >>> for secondary_instrument in instrumenttools.Instrument.\
            ...     list_secondary_instruments()[:5]:
            ...     secondary_instrument
            ...
            <class 'abjad.tools.instrumenttools.AltoFlute.AltoFlute.AltoFlute'>
            <class 'abjad.tools.instrumenttools.AltoTrombone.AltoTrombone.AltoTrombone'>
            <class 'abjad.tools.instrumenttools.BaritoneSaxophone.BaritoneSaxophone.BaritoneSaxophone'>
            <class 'abjad.tools.instrumenttools.BassClarinet.BassClarinet.BassClarinet'>
            <class 'abjad.tools.instrumenttools.BassFlute.BassFlute.BassFlute'>

        Return list
        '''
        secondary_instruments = []
        for instrument_class in cls.list_instruments():
            instrument = instrument_class()
            if instrument.is_secondary_instrument:
                secondary_instruments.append(instrument_class)
        return secondary_instruments
