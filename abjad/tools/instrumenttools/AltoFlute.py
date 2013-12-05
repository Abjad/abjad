# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


class AltoFlute(Instrument):
    r'''An alto flute.

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> alto_flute = instrumenttools.AltoFlute()
        >>> attach(alto_flute, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Alto flute }
            \set Staff.shortInstrumentName = \markup { Alt. fl. }
            c'4
            d'4
            e'4
            f'4
        }

    The alto flute targets the staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(
        self,
        instrument_name='alto flute',
        short_instrument_name='alt. fl.',
        instrument_name_markup=None,
        short_instrument_name_markup=None,
        allowable_clefs=None,
        pitch_range=None,
        sounding_pitch_of_written_middle_c='g',
        ):
        pitch_range = pitch_range or pitchtools.PitchRange(-5, 31)
        Instrument.__init__(
            self,
            instrument_name=instrument_name,
            short_instrument_name=short_instrument_name,
            instrument_name_markup=instrument_name_markup,
            short_instrument_name_markup=short_instrument_name_markup,
            allowable_clefs=allowable_clefs,
            pitch_range=pitch_range,
            sounding_pitch_of_written_middle_c=\
                sounding_pitch_of_written_middle_c,
            )
        self._performer_names.extend([
            'wind player',
            'flautist',
            'flutist',
            ])
        self._starting_clefs = indicatortools.ClefInventory(['treble'])

#    ### SPECIAL METHODS ###
#
#    def __format__(self, format_specification=''):
#        r'''Formats alto flute.
#
#        Set `format_specification` to `''` or `'storage'`.
#        Interprets `''` equal to `'storage'`.
#
#        ..  container:: example
#
#            Without customization:
#
#            ::
#
#                >>> alto_flute = instrumenttools.AltoFlute()
#                >>> print format(alto_flute)
#                instrumenttools.AltoFlute()
#
#        ..  container:: example
#
#            With customization:
#
#            ::
#
#                >>> custom = instrumenttools.AltoFlute()
#                >>> custom.instrument_name = 'flauto contralto'
#                >>> markup = markuptools.Markup('Flauto contralto')
#                >>> custom.instrument_name_markup = markup
#                >>> custom.short_instrument_name = 'fl. contr.'
#                >>> markup = markuptools.Markup('Fl. contr.')
#                >>> custom.short_instrument_name_markup = markup
#                >>> custom.pitch_range = '[G3, C7]'
#
#            ::
#
#                >>> print format(custom)
#                instrumenttools.AltoFlute(
#                    instrument_name='flauto contralto',
#                    instrument_name_markup=markuptools.Markup(
#                        ('Flauto contralto',)
#                        ),
#                    short_instrument_name='fl. contr.',
#                    short_instrument_name_markup=markuptools.Markup(
#                        ('Fl. contr.',)
#                        ),
#                    pitch_range=pitchtools.PitchRange(
#                        '[G3, C7]'
#                        ),
#                    )
#
#        Returns string.
#        '''
#        superclass = super(AltoFlute, self)
#        return superclass.__format__(format_specification=format_specification)
#
#    ### PUBLIC PROPERTIES ###
#
#    @property
#    def allowable_clefs(self):
#        r'''Gets and sets allowable clefs.
#
#        ..  container:: example
#
#            Gets property:
#
#            ::
#
#                >>> alto_flute.allowable_clefs
#                ClefInventory([Clef('treble')])
#
#            ::
#
#                >>> import copy
#                >>> skips = []
#                >>> for clef in alto_flute.allowable_clefs:
#                ...     skip = scoretools.Skip((1, 8))
#                ...     clef = copy.copy(clef)
#                ...     attach(clef, skip)
#                ...     skips.append(skip)
#                >>> staff = Staff(skips)
#                >>> override(staff).clef.full_size_change = True
#                >>> override(staff).time_signature.stencil = False
#                >>> show(staff) # doctest: +SKIP
#
#        ..  container:: example
#
#            Sets property:
#
#            ::
#
#                >>> alto_flute.allowable_clefs = ['treble', 'treble^8']
#                >>> alto_flute.allowable_clefs
#                ClefInventory([Clef('treble'), Clef('treble^8')])
#
#        ..  container:: example
#
#            Restores default:
#
#            ::
#
#                >>> alto_flute.allowable_clefs = None
#                >>> alto_flute.allowable_clefs
#                ClefInventory([Clef('treble')])
#
#        Returns clef inventory.
#        '''
#        return Instrument.allowable_clefs.fget(self)
#
#    @allowable_clefs.setter
#    def allowable_clefs(self, allowable_clefs):
#        return Instrument.allowable_clefs.fset(self, allowable_clefs)
#
#    @property
#    def instrument_name(self):
#        r'''Gets and sets instrument name.
#
#        ..  container:: example
#
#            Gets property:
#
#            ::
#
#                >>> alto_flute.instrument_name
#                'alto flute'
#
#        ..  container:: example
#
#            Sets property:
#
#            ::
#
#                >>> alto_flute.instrument_name = 'flauto contralto'
#                >>> alto_flute.instrument_name
#                'flauto contralto'
#
#        ..  container:: example
#
#            Restores default:
#
#            ::
#
#                >>> alto_flute.instrument_name = None
#                >>> alto_flute.instrument_name
#                'alto flute'
#
#        Returns string.
#        '''
#        return Instrument.instrument_name.fget(self)
#
#    @instrument_name.setter
#    def instrument_name(self, foo):
#        Instrument.instrument_name.fset(self, foo)
#
#    @property
#    def instrument_name_markup(self):
#        r'''Gets and sets instrument name markup.
#
#        ..  container:: example
#
#            Gets property:
#
#            ::
#
#                >>> alto_flute.instrument_name_markup
#                Markup(('Alto flute',))
#
#        ..  container:: example
#
#            Sets property:
#
#            ::
#
#                >>> markup = markuptools.Markup('Flauto contralto')
#                >>> alto_flute.instrument_name_markup = markup
#                >>> alto_flute.instrument_name_markup
#                Markup(('Flauto contralto',))
#
#        ..  container:: example
#
#            Restores default:
#
#            ::
#
#                >>> alto_flute.instrument_name_markup = None
#                >>> alto_flute.instrument_name_markup
#                Markup(('Alto flute',))
#
#        Returns markup.
#        '''
#        return Instrument.instrument_name_markup.fget(self)
#
#    @instrument_name_markup.setter
#    def instrument_name_markup(self, markup):
#        return Instrument.instrument_name_markup.fset(self, markup)
#
#    @property
#    def pitch_range(self):
#        r"""Gets and sets pitch range.
#
#        ..  container:: example
#
#            Gets property:
#
#            ::
#
#                >>> alto_flute.pitch_range
#                PitchRange('[G3, G6]')
#
#            ::
#
#                >>> chord = Chord("<c' d'>1")
#                >>> start_pitch = alto_flute.pitch_range.start_pitch
#                >>> chord.note_heads[0].written_pitch = start_pitch
#                >>> stop_pitch = alto_flute.pitch_range.stop_pitch
#                >>> chord.note_heads[1].written_pitch = stop_pitch
#                >>> voice = Voice([chord])
#                >>> staff = Staff([voice])
#                >>> override(staff).time_signature.stencil = False
#                >>> show(staff) # doctest: +SKIP
#
#        ..  container:: example
#
#            Sets property:
#
#            ::
#
#                >>> alto_flute.pitch_range = '[G3, C7]'
#                >>> alto_flute.pitch_range
#                PitchRange('[G3, C7]')
#
#        ..  container:: example
#
#            Restores default:
#
#            ::
#
#                >>> alto_flute.pitch_range = None
#                >>> alto_flute.pitch_range
#                PitchRange('[G3, G6]')
#
#        Returns pitch range.
#        """
#        return Instrument.pitch_range.fget(self)
#
#    @pitch_range.setter
#    def pitch_range(self, pitch_range):
#        Instrument.pitch_range.fset(self, pitch_range)
#
#    @property
#    def short_instrument_name(self):
#        r'''Gets and sets short instrument name.
#
#        ..  container:: example
#
#            Gets property:
#        
#            ::
#
#                >>> alto_flute.short_instrument_name
#                'alt. fl.'
#
#        ..  container:: example
#
#            Sets property:
#    
#            ::
#
#                >>> alto_flute.short_instrument_name = 'fl. contr.'
#                >>> alto_flute.short_instrument_name
#                'fl. contr.'
#
#        ..  container:: example
#
#            Restores default:
#
#            ::
#
#                >>> alto_flute.short_instrument_name = None
#                >>> alto_flute.short_instrument_name
#                'alt. fl.'
#
#        Returns string.
#        '''
#        return Instrument.short_instrument_name.fget(self)
#
#    @short_instrument_name.setter
#    def short_instrument_name(self, name):
#        return Instrument.short_instrument_name.fset(self, name)
#
#    @property
#    def short_instrument_name_markup(self):
#        r'''Gets and sets short instrument name markup.
#
#        ..  container:: example
#
#            Gets property:
#
#            ::
#
#                >>> alto_flute.short_instrument_name_markup
#                Markup(('Alt. fl.',))
#
#        ..  container:: example
#
#            Sets property:
#
#            ::
#
#                >>> markup = markuptools.Markup('Fl. contr.')
#                >>> alto_flute.short_instrument_name_markup = markup
#                >>> alto_flute.short_instrument_name_markup
#                Markup(('Fl. contr.',))
#
#        ..  container:: example
#
#            Restores default:
#
#            ::
#
#                >>> alto_flute.short_instrument_name_markup = None
#                >>> alto_flute.short_instrument_name_markup
#                Markup(('Alt. fl.',))
#
#        Returns markup.
#        '''
#        return Instrument.short_instrument_name_markup.fget(self)
#
#    @short_instrument_name_markup.setter
#    def short_instrument_name_markup(self, markup):
#        return Instrument.short_instrument_name_markup.fset(self, markup)
#
#    @property
#    def sounding_pitch_of_written_middle_c(self):
#        r'''Gets and sets sounding pitch of written middle C.
#
#        ..  container:: example
#
#            Gets property:
#
#            ::
#
#                >>> alto_flute.sounding_pitch_of_written_middle_c
#                NamedPitch('g')
#
#            ::
#
#                >>> pitch = alto_flute.sounding_pitch_of_written_middle_c
#                >>> note = Note(pitch, Duration(1))
#                >>> voice = Voice([note])
#                >>> staff = Staff([voice])
#                >>> override(staff).time_signature.stencil = False
#                >>> show(staff) # doctest: +SKIP
#
#        ..  container:: example
#
#            Sets property:
#
#            ::
#
#                >>> alto_flute.sounding_pitch_of_written_middle_c = 'gs'
#                >>> alto_flute.sounding_pitch_of_written_middle_c
#                NamedPitch('gs')
#
#        ..  container:: example
#
#            Restores default:
#
#            ::
#
#                >>> alto_flute.sounding_pitch_of_written_middle_c = None
#                >>> alto_flute.sounding_pitch_of_written_middle_c
#                NamedPitch('g')
#
#        Returns named pitch.
#        '''
#        return Instrument.sounding_pitch_of_written_middle_c.fget(self)
#
#    @sounding_pitch_of_written_middle_c.setter
#    def sounding_pitch_of_written_middle_c(self, pitch):
#        return Instrument.sounding_pitch_of_written_middle_c.fset(
#            self, pitch)
