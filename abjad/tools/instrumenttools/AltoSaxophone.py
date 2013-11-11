# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class AltoSaxophone(Instrument):
    r'''An alto saxophone.

    ::

        >>> staff = Staff("c'4 d'4 e'4 f'4")
        >>> alto_sax = instrumenttools.AltoSaxophone()
        >>> attach(alto_sax, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.instrumentName = \markup { Alto saxophone }
            \set Staff.shortInstrumentName = \markup { Alt. sax. }
            c'4
            d'4
            e'4
            f'4
        }

    The alto saxophone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        pitch = pitchtools.NamedPitch('ef')
        self._default_instrument_name = 'alto saxophone'
        self._default_performer_names.extend([
            'wind player',
            'reed player',
            'single reed player',
            'saxophonist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(-11, 21)
        self._default_short_instrument_name = 'alt. sax.'
        self._default_sounding_pitch_of_written_middle_c = pitch
        self._is_primary_instrument = True

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats alto sax.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            Without customization:

            ::

                >>> alto_sax = instrumenttools.AltoSaxophone()
                >>> print format(alto_sax)
                instrumenttools.AltoSaxophone()

        ..  container:: example

            With customization:

            ::

                >>> custom = instrumenttools.AltoSaxophone()
                >>> custom.instrument_name = 'sassofono contralto'
                >>> markup = markuptools.Markup('Sassofono contralto')
                >>> custom.instrument_name_markup = markup
                >>> custom.short_instrument_name = 'sass. contr.'
                >>> markup = markuptools.Markup('Sass. contr.')
                >>> custom.short_instrument_name_markup = markup
                >>> custom.pitch_range = '[G3, C7]'

            ::

                >>> print format(custom)
                instrumenttools.AltoSaxophone(
                    instrument_name='sassofono contralto',
                    instrument_name_markup=markuptools.Markup((
                        'Sassofono contralto',
                        )),
                    short_instrument_name='sass. contr.',
                    short_instrument_name_markup=markuptools.Markup((
                        'Sass. contr.',
                        )),
                    pitch_range=pitchtools.PitchRange(
                        '[G3, C7]'
                        )
                    )

        Returns string.
        '''
        superclass = super(AltoSaxophone, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @apply
    def allowable_clefs():
        def fget(self):
            r'''Gets and sets allowable clefs.

            ..  container:: example

                Gets property:

                ::

                    >>> alto_sax.allowable_clefs
                    ClefInventory([Clef('treble')])

                :: 

                    >>> import copy
                    >>> skips = []
                    >>> for clef in alto_sax.allowable_clefs:
                    ...     skip = scoretools.Skip((1, 8))
                    ...     clef = copy.copy(clef)
                    ...     attach(clef, skip)
                    ...     skips.append(skip)
                    >>> staff = Staff(skips)
                    >>> override(staff).clef.full_size_change = True
                    >>> override(staff).time_signature.stencil = False
                    >>> show(staff) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> alto_sax.allowable_clefs = ['treble', 'treble^8']
                    >>> alto_sax.allowable_clefs
                    ClefInventory([Clef('treble'), Clef('treble^8')])

            ..  container:: example

                Restores default:

                ::

                    >>> alto_sax.allowable_clefs = None
                    >>> alto_sax.allowable_clefs
                    ClefInventory([Clef('treble')])

            Returns clef inventory.
            '''
            return Instrument.allowable_clefs.fget(self)
        def fset(self, allowable_clefs):
            return Instrument.allowable_clefs.fset(self, allowable_clefs)
        return property(**locals())

    @apply
    def instrument_name():
        def fget(self):
            r'''Gets and sets instrument name.

            ..  container:: example

                Gets property:

                ::

                    >>> alto_sax.instrument_name
                    'alto saxophone'

            ..  container:: example

                Sets property:

                ::

                    >>> alto_sax.instrument_name = 'sassofono contralto'
                    >>> alto_sax.instrument_name
                    'sassofono contralto'

            ..  container:: example

                Restores default:

                ::

                    >>> alto_sax.instrument_name = None
                    >>> alto_sax.instrument_name
                    'alto saxophone'

            Returns string.
            '''
            return Instrument.instrument_name.fget(self)
        def fset(self, foo):
            Instrument.instrument_name.fset(self, foo)
        return property(**locals())

    @apply
    def instrument_name_markup():
        def fget(self):
            r'''Gets and sets instrument name markup.

            ..  container:: example

                Gets property:

                ::

                    >>> alto_sax.instrument_name_markup
                    Markup(('Alto saxophone',))

            ..  container:: example

                Sets property:

                ::

                    >>> markup = markuptools.Markup('Sassofono contralto')
                    >>> alto_sax.instrument_name_markup = markup
                    >>> alto_sax.instrument_name_markup
                    Markup(('Sassofono contralto',))

            ..  container:: example

                Restores default:

                ::

                    >>> alto_sax.instrument_name_markup = None
                    >>> alto_sax.instrument_name_markup
                    Markup(('Alto saxophone',))

            Returns markup.
            '''
            return Instrument.instrument_name_markup.fget(self)
        def fset(self, markup):
            return Instrument.instrument_name_markup.fset(self, markup)
        return property(**locals())

    @apply
    def pitch_range():
        def fget(self):
            r"""Gets and sets pitch range.

            ..  container:: example

                Gets property:

                ::

                    >>> alto_sax.pitch_range
                    PitchRange('[C#3, A5]')

                ::

                    >>> chord = Chord("<c' d'>1")
                    >>> start_pitch = alto_sax.pitch_range.start_pitch
                    >>> chord.note_heads[0].written_pitch = start_pitch
                    >>> stop_pitch = alto_sax.pitch_range.stop_pitch
                    >>> chord.note_heads[1].written_pitch = stop_pitch
                    >>> voice = Voice([chord])
                    >>> staff = Staff([voice])
                    >>> override(staff).time_signature.stencil = False
                    >>> show(staff) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> alto_sax.pitch_range = '[C#3, A6]'
                    >>> alto_sax.pitch_range
                    PitchRange('[C#3, A6]')

            ..  container:: example

                Restores default:

                ::

                    >>> alto_sax.pitch_range = None
                    >>> alto_sax.pitch_range
                    PitchRange('[C#3, A5]')

            Returns pitch range.
            """
            return Instrument.pitch_range.fget(self)
        def fset(self, pitch_range):
            Instrument.pitch_range.fset(self, pitch_range)
        return property(**locals())

    @apply
    def short_instrument_name():
        def fget(self):
            r'''Gets and sets short instrument name.

            ..  container:: example

                Gets property:

                ::

                    >>> alto_sax.short_instrument_name
                    'alt. sax.'
    
            ..  container:: example

                Sets property:

                ::

                    >>> alto_sax.short_instrument_name = 'sass. contr.'
                    >>> alto_sax.short_instrument_name
                    'sass. contr.'

            ..  container:: example

                Restores default:

                ::

                    >>> alto_sax.short_instrument_name = None
                    >>> alto_sax.short_instrument_name
                    'alt. sax.'

            Returns string.
            '''
            return Instrument.short_instrument_name.fget(self)
        def fset(self, name):
            return Instrument.short_instrument_name.fset(self, name)
        return property(**locals())

    @apply
    def short_instrument_name_markup():
        def fget(self):
            r'''Gets and sets short instrument name markup.

            ..  container:: example

                Gets property:

                ::

                    >>> alto_sax.short_instrument_name_markup
                    Markup(('Alt. sax.',))

            ..  container:: example

                Sets property:

                ::

                    >>> markup = markuptools.Markup('Sass. contr.')
                    >>> alto_sax.short_instrument_name_markup = markup
                    >>> alto_sax.short_instrument_name_markup
                    Markup(('Sass. contr.',))

            ..  container:: example

                Restores default:

                ::

                    >>> alto_sax.short_instrument_name_markup = None
                    >>> alto_sax.short_instrument_name_markup
                    Markup(('Alt. sax.',))

            Returns markup.
            '''
            return Instrument.short_instrument_name_markup.fget(self)
        def fset(self, markup):
            return Instrument.short_instrument_name_markup.fset(self, markup)
        return property(**locals())

    @apply
    def sounding_pitch_of_written_middle_c():
        def fget(self):
            r'''Gets and sets sounding pitch of written middle C.

            ..  container:: example

                Gets property:

                ::

                    >>> alto_sax.sounding_pitch_of_written_middle_c
                    NamedPitch('ef')

            ..  container:: example

                Sets property:

                ::

                    >>> alto_sax.sounding_pitch_of_written_middle_c = 'e'
                    >>> alto_sax.sounding_pitch_of_written_middle_c
                    NamedPitch('e')

            ..  container:: example

                Restores default:

                ::

                    >>> alto_sax.sounding_pitch_of_written_middle_c = None
                    >>> alto_sax.sounding_pitch_of_written_middle_c
                    NamedPitch('ef')

            Returns named pitch.
            '''
            return Instrument.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
