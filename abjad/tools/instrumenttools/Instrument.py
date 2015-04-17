# -*- encoding: utf-8 -*-
import copy
import inspect
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools import stringtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Instrument(AbjadObject):
    '''A musical instrument.
    '''

    ### CLASS VARIABLES ###

    _format_slot = 'opening'

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
        from abjad.tools import scoretools
        self._do_not_format = False
        self._instrument_name = instrument_name
        self._instrument_name_markup = instrument_name_markup
        self._short_instrument_name = short_instrument_name
        self._short_instrument_name_markup = short_instrument_name_markup
        allowable_clefs = allowable_clefs or ['treble']
        allowable_clefs = indicatortools.ClefInventory(allowable_clefs)
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

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies instrument.

        Returns new instrument.
        '''
        return type(self)(
            instrument_name=self.instrument_name,
            short_instrument_name=self.short_instrument_name,
            instrument_name_markup=self.instrument_name_markup,
            short_instrument_name_markup=self.short_instrument_name_markup,
            allowable_clefs=self.allowable_clefs,
            pitch_range=self.pitch_range,
            sounding_pitch_of_written_middle_c=\
                self.sounding_pitch_of_written_middle_c,
            )

    def __eq__(self, arg):
        r'''Is true when `arg` is an instrument with instrument name and short
        instrument name equal to those of this instrument. Otherwise false.

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.instrument_name == arg.instrument_name and \
                self.short_instrument_name == arg.short_instrument_name:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats instrument.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __hash__(self):
        '''Gets hash value instrument.

        Computed on type, instrument name and short instrument name.

        Returns integer.
        '''
        return hash((
            type(self).__name__,
            self.instrument_name,
            self.short_instrument_name,
            ))

    def __repr__(self):
        r'''Gets interpreter representation of instrument.

        Returns string.
        '''
        return '{}()'.format(type(self).__name__)

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import indicatortools
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='allowable_clefs',
                display_string='clefs',
                command='cf',
                editor=indicatortools.ClefInventory,
                ),
            systemtools.AttributeDetail(
                name='instrument_name',
                command='in',
                editor=idetools.getters.get_string,
                ),
            systemtools.AttributeDetail(
                name='instrument_name_markup',
                command='im',
                editor=idetools.getters.get_markup,
                ),
            systemtools.AttributeDetail(
                name='pitch_range',
                display_string='range',
                command='rg',
                editor=idetools.getters.get_pitch_range_string,
                ),
            systemtools.AttributeDetail(
                name='short_instrument_name',
                command='sn',
                editor=idetools.getters.get_string,
                ),
            systemtools.AttributeDetail(
                name='short_instrument_name_markup',
                command='sm',
                editor=idetools.getters.get_markup,
                ),
            systemtools.AttributeDetail(
                name='sounding_pitch_of_written_middle_c',
                display_string='sounding pitch of written middle C',
                command='sp',
                editor=idetools.getters.get_named_pitch,
                ),
            )

    @staticmethod
    def _default_instrument_name_to_instrument_class(default_instrument_name):
        for instrument_class in Instrument._list_instruments():
            instrument = instrument_class()
            if instrument.instrument_name == default_instrument_name:
                return instrument_class

    # TODO: _scope_name needs to be taken from IndicatorExpression!
    #       should not be stored on instrument.
    @property
    def _lilypond_format(self):
        result = []
        if self._do_not_format:
            return result
        line = r'\set {!s}.instrumentName = {!s}'
        line = line.format(
            self._scope_name,
            self.instrument_name_markup,
            )
        result.append(line)
        line = r'\set {!s}.shortInstrumentName = {!s}'
        line = line.format(
            self._scope_name,
            self.short_instrument_name_markup,
            )
        result.append(line)
        return result

    @property
    def _one_line_menu_summary(self):
        return self.instrument_name

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
                string = stringtools.capitalize_start(string)
                markup = markuptools.Markup(contents=string)
                self._instrument_name_markup = markup
            else:
                self._instrument_name_markup = None
        if self._short_instrument_name_markup is None:
            if self.short_instrument_name:
                string = self.short_instrument_name
                string = stringtools.capitalize_start(string)
                markup = markuptools.Markup(contents=string)
                self._short_instrument_name_markup = markup
            else:
                self._short_instrument_name_markup = None

    @classmethod
    def _list_instrument_names(cls):
        r'''Lists instrument names.

        ::

            >>> function = instrumenttools.Instrument._list_instrument_names
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
        for instrument_class in cls._list_instruments():
            instrument = instrument_class()
            assert instrument.instrument_name is not None, repr(instrument)
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
                    if not value is instrumenttools.Instrument:
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

    @property
    def allowable_clefs(self):
        r'''Gets allowable clefs of instrument.

        Returns clef inventory.
        '''
        if self._allowable_clefs is None:
            self._allowable_clefs = indicatortools.ClefInventory('treble')
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

    def transpose_from_sounding_pitch_to_written_pitch(self, note_or_chord):
        r'''Transposes `note_or_chord` from sounding pitch of instrument to
        written pitch of instrument.

        Returns `note_or_chord` with adjusted pitches.
        '''
        from abjad.tools import scoretools
        sounding_pitch = self.sounding_pitch_of_written_middle_c
        index = pitchtools.NamedPitch('C4') - sounding_pitch
        index *= -1
        if isinstance(note_or_chord, scoretools.Note):
            note_or_chord.written_pitch = \
                pitchtools.transpose_pitch_carrier_by_interval(
                    note_or_chord.written_pitch, index)
        elif isinstance(note_or_chord, scoretools.Chord):
            pitches = [
                pitchtools.transpose_pitch_carrier_by_interval(pitch, index)
                for pitch in note_or_chord.written_pitches
                ]
            note_or_chord.written_pitches = pitches
        else:
            message = 'must be note or chord: {!r}.'
            message = message.format(note_or_chord)
            raise TypeError(message)

    def transpose_from_written_pitch_to_sounding_pitch(self, note_or_chord):
        r'''Transposes `expr` from written pitch of instrument to sounding
        pitch of instrument.

        Returns `note_or_chord` with adjusted pitches.
        '''
        from abjad.tools import scoretools
        sounding_pitch = self.sounding_pitch_of_written_middle_c
        index = pitchtools.NamedPitch('C4') - sounding_pitch
        if isinstance(note_or_chord, scoretools.Note):
            note_or_chord.written_pitch = \
                pitchtools.transpose_pitch_carrier_by_interval(
                    note_or_chord.written_pitch, index)
        elif isinstance(note_or_chord, scoretools.Chord):
            pitches = [
                pitchtools.transpose_pitch_carrier_by_interval(pitch, index)
                for pitch in note_or_chord.written_pitches
                ]
            note_or_chord.written_pitches = pitches