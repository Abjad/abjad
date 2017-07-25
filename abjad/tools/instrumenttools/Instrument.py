# -*- coding: utf-8 -*-
import copy
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import datastructuretools
from abjad.tools import systemtools
from abjad.tools.topleveltools import new
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Instrument(AbjadValueObject):
    '''Instrument.

    ::

        >>> import abjad

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allowable_clefs',
        '_default_scope',
        '_do_not_format',
        '_instrument_name',
        '_instrument_name_markup',
        '_is_primary_instrument',
        '_performer_names',
        '_pitch_range',
        '_short_instrument_name',
        '_short_instrument_name_markup',
        '_sounding_pitch_of_written_middle_c',
        '_starting_clefs',
        )

    _format_slot = 'opening'

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name=None,
        short_instrument_name=None,
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c=None,
        ):
        from abjad.tools import instrumenttools
        from abjad.tools import scoretools
        self._do_not_format = False
        if instrument_name is not None:
            instrument_name = str(instrument_name)
        self._instrument_name = instrument_name
        if instrument_name_markup is not None:
            instrument_name_markup = markuptools.Markup(
                instrument_name_markup)
        self._instrument_name_markup = instrument_name_markup
        if short_instrument_name is not None:
            short_instrument_name = str(short_instrument_name)
        self._short_instrument_name = short_instrument_name
        if short_instrument_name_markup is not None:
            short_instrument_name_markup = markuptools.Markup(
                short_instrument_name_markup)
        self._short_instrument_name_markup = short_instrument_name_markup
        allowable_clefs = allowable_clefs or ['treble']
        allowable_clefs = instrumenttools.ClefList(allowable_clefs)
        self._allowable_clefs = allowable_clefs
        if isinstance(pitch_range, str):
            pitch_range = pitchtools.PitchRange(pitch_range)
        elif isinstance(pitch_range, pitchtools.PitchRange):
            pitch_range = copy.copy(pitch_range)
        elif pitch_range is None:
            pitch_range = pitchtools.PitchRange()
        else:
            raise TypeError(pitch_range)
        self._pitch_range = pitch_range
        sounding_pitch_of_written_middle_c = \
            sounding_pitch_of_written_middle_c or pitchtools.NamedPitch("c'")
        sounding_pitch_of_written_middle_c = \
            pitchtools.NamedPitch(sounding_pitch_of_written_middle_c)
        self._sounding_pitch_of_written_middle_c = \
            sounding_pitch_of_written_middle_c
        self._default_scope = scoretools.Staff
        self._is_primary_instrument = False
        self._performer_names = ['instrumentalist']
        self._starting_clefs = copy.copy(allowable_clefs)

    ### PRIVATE PROPERTIES ###

    @staticmethod
    def _default_instrument_name_to_instrument_class(default_instrument_name):
        for instrument_class in Instrument._list_instruments():
            instrument = instrument_class()
            if instrument.instrument_name == default_instrument_name:
                return instrument_class

    @property
    def _scope_name(self):
        if isinstance(self._default_scope, type):
            return self._default_scope.__name__
        elif isinstance(self._default_scope, str):
            return self._default_scope
        else:
            return type(self._default_scope).__name__

    ### PRIVATE METHODS ###

    def _get_default_performer_name(self):
        if self._performer_names is None:
            performer_name = '{} player'.format(self._default_instrument_name)
            return performer_name
        else:
            return self._performer_names[-1]

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            self,
            repr_args_values=[],
            repr_is_indented=False,
            repr_kwargs_names=[],
            )

    # TODO: _scope_name needs to be taken from IndicatorWrapper!
    #       should not be stored on instrument.
    def _get_lilypond_format(self):
        result = []
        if self._do_not_format:
            return result
        instrument_name_markup = self.instrument_name_markup
        if instrument_name_markup.direction is not None:
            instrument_name_markup = new(
                instrument_name_markup,
                direction=None,
                )
        line = r'\set {!s}.instrumentName = {!s}'
        line = line.format(
            self._scope_name,
            instrument_name_markup,
            )
        result.append(line)
        line = r'\set {!s}.shortInstrumentName = {!s}'
        short_instrument_name_markup = self.short_instrument_name_markup
        if short_instrument_name_markup.direction is not None:
            short_instrument_name_markup = new(
                short_instrument_name_markup,
                direction=None,
                )
        line = line.format(
            self._scope_name,
            short_instrument_name_markup,
            )
        result.append(line)
        return result

    def _get_performer_names(self):
        if self._performer_names is None:
            performer_name = '{} player'.format(self._default_instrument_name)
            return [performer_name]
        else:
            return self._performer_names[:]

    def _initialize_default_name_markups(self):
        if self._instrument_name_markup is None:
            if self.instrument_name:
                string = self.instrument_name
                string = datastructuretools.String(string).capitalize_start()
                markup = markuptools.Markup(contents=string)
                self._instrument_name_markup = markup
            else:
                self._instrument_name_markup = None
        if self._short_instrument_name_markup is None:
            if self.short_instrument_name:
                string = self.short_instrument_name
                string = datastructuretools.String(string).capitalize_start()
                markup = markuptools.Markup(contents=string)
                self._short_instrument_name_markup = markup
            else:
                self._short_instrument_name_markup = None

    @classmethod
    def _list_instrument_names(class_):
        r'''Lists instrument names.

        ::

            >>> function = abjad.instrumenttools.Instrument._list_instrument_names
            >>> for instrument_name in function():
            ...     instrument_name
            ...
            'accordion'
            'alto'
            'alto flute'
            ...

        Returns list.
        '''
        instrument_names = []
        for instrument_class in class_._list_instruments():
            instrument = instrument_class()
            assert instrument.instrument_name is not None, repr(instrument)
            instrument_names.append(instrument.instrument_name)
        instrument_names.sort(key=lambda x: x.lower())
        return instrument_names

    @staticmethod
    def _list_instruments(classes=None):
        r'''Lists instruments.

        ::

            >>> function = abjad.instrumenttools.Instrument._list_instruments
            >>> for instrument in function():
            ...     instrument.__name__
            ...
            'Accordion'
            'AltoFlute'
            'AltoSaxophone'
            'AltoTrombone'
            'AltoVoice'
            'BaritoneSaxophone'
            ...

        Returns list.
        '''
        from abjad.tools import instrumenttools
        if classes is None:
            classes = (instrumenttools.Instrument,)
        instruments = []
        for value in instrumenttools.__dict__.values():
            try:
                if issubclass(value, classes):
                    if value is not instrumenttools.Instrument:
                        instruments.append(value)
            except TypeError:
                pass
        instruments.sort(key=lambda x: x.__name__.lower())
        return instruments

    @classmethod
    def _list_primary_instruments(class_):
        primary_instruments = []
        for instrument_class in class_._list_instruments():
            instrument = instrument_class()
            if instrument._is_primary_instrument:
                primary_instruments.append(instrument_class)
        return primary_instruments

    @classmethod
    def _list_secondary_instruments(class_):
        secondary_instruments = []
        for instrument_class in class_._list_instruments():
            instrument = instrument_class()
            if not instrument._is_primary_instrument:
                secondary_instruments.append(instrument_class)
        return secondary_instruments

    ### PUBLIC PROPERTIES ###

    @property
    def allowable_clefs(self):
        r'''Gets allowable clefs of instrument.

        Returns clef list.
        '''
        if self._allowable_clefs is None:
            self._allowable_clefs = abjad.instrumenttools.ClefList('treble')
        return self._allowable_clefs

    @property
    def instrument_name(self):
        r'''Gets instrument name.

        Returns string.
        '''
        return self._instrument_name

    @property
    def instrument_name_markup(self):
        r'''Gets instrument name markup.

        Returns markup.
        '''
        if self._instrument_name_markup is None:
            self._initialize_default_name_markups()
        if not isinstance(self._instrument_name_markup, markuptools.Markup):
            markup = markuptools.Markup(contents=self._instrument_name_markup)
            self._instrument_name_markup = markup
        if self._instrument_name_markup.contents != ('',):
            return self._instrument_name_markup

    @property
    def pitch_range(self):
        r'''Gets pitch range of instrument.

        Returns pitch range.
        '''
        return self._pitch_range

    @property
    def short_instrument_name(self):
        r'''Gets short instrument name.

        Returns string.
        '''
        return self._short_instrument_name

    @property
    def short_instrument_name_markup(self):
        r'''Gets short instrument name markup.

        Returns markup.
        '''
        if self._short_instrument_name_markup is None:
            self._initialize_default_name_markups()
        if not isinstance(
            self._short_instrument_name_markup, markuptools.Markup):
            markup = markuptools.Markup(
                contents=self._short_instrument_name_markup)
            self._short_instrument_name_markup = markup
        if self._short_instrument_name_markup.contents != ('',):
            return self._short_instrument_name_markup

    @property
    def sounding_pitch_of_written_middle_c(self):
        r'''Gets sounding pitch of written middle C.

        Returns named pitch.
        '''
        return self._sounding_pitch_of_written_middle_c

    ### PUBLIC METHODS ###

    @staticmethod
    def transpose_from_sounding_pitch(argument):
        r'''Transpose notes and chords in `argument` from sounding pitch
        to written pitch:

        ..  container:: example

            ::

                >>> staff = abjad.Staff("<c' e' g'>4 d'4 r4 e'4")
                >>> clarinet = abjad.instrumenttools.ClarinetInBFlat()
                >>> abjad.attach(clarinet, staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
                    <c' e' g'>4
                    d'4
                    r4
                    e'4
                }

            ::

                >>> abjad.Instrument.transpose_from_sounding_pitch(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
                    <d' fs' a'>4
                    e'4
                    r4
                    fs'4
                }

        Returns none.
        '''
        import abjad
        for leaf in abjad.iterate(argument).by_leaf(pitched=True):
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if not instrument:
                continue
            sounding_pitch = instrument.sounding_pitch_of_written_middle_c
            interval = abjad.NamedPitch('C4') - sounding_pitch
            interval *= -1
            if isinstance(leaf, abjad.Note):
                pitch = leaf.written_pitch
                pitch = interval.transpose(pitch)
                leaf.written_pitch = pitch
            elif isinstance(leaf, abjad.Chord):
                pitches = [
                    interval.transpose(pitch)
                    for pitch in leaf.written_pitches
                    ]
                leaf.written_pitches = pitches

    @staticmethod
    def transpose_from_written_pitch(argument):
        r'''Transposes notes and chords in `argument` from sounding pitch
        to written pitch.

        ..  container:: example

            ::

                >>> staff = abjad.Staff("<c' e' g'>4 d'4 r4 e'4")
                >>> clarinet = abjad.instrumenttools.ClarinetInBFlat()
                >>> abjad.attach(clarinet, staff[0])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
                    <c' e' g'>4
                    d'4
                    r4
                    e'4
                }

            ::

                >>> abjad.Instrument.transpose_from_written_pitch(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }
                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }
                    <bf d' f'>4
                    c'4
                    r4
                    d'4
                }

        Returns none.
        '''
        import abjad
        for leaf in abjad.iterate(argument).by_leaf(pitched=True):
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if not instrument:
                continue
            sounding_pitch = instrument.sounding_pitch_of_written_middle_c
            interval = abjad.NamedPitch('C4') - sounding_pitch
            if isinstance(leaf, abjad.Note):
                written_pitch = leaf.written_pitch
                written_pitch = interval.transpose(written_pitch)
                leaf.written_pitch = written_pitch
            elif isinstance(leaf, abjad.Chord):
                pitches = [
                    interval.transpose(pitch)
                    for pitch in leaf.written_pitches
                    ]
                leaf.written_pitches = pitches
