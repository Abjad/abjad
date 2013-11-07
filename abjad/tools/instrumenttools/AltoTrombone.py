# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import markuptools
from abjad.tools import pitchtools
from abjad.tools.instrumenttools.Instrument import Instrument


class AltoTrombone(Instrument):
    r'''An alto trombone.

    ::

        >>> staff = Staff("c4 d4 e4 f4")
        >>> clef = marktools.ClefMark('bass')
        >>> clef = attach(clef, staff)
        >>> alto_trombone = instrumenttools.AltoTrombone()
        >>> alto_trombone = attach(alto_trombone, staff)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "bass"
            \set Staff.instrumentName = \markup { Alto trombone }
            \set Staff.shortInstrumentName = \markup { Alt. trb. }
            c4
            d4
            e4
            f4
        }

    The alto trombone targets staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_allowable_clefs = marktools.ClefMarkInventory([
            marktools.ClefMark('bass'), 
            marktools.ClefMark('tenor'),
            ])
        self._default_instrument_name = 'alto trombone'
        self._default_performer_names.extend([
            'brass player',
            'trombonist',
            ])
        self._default_pitch_range = pitchtools.PitchRange('[A2, Bb5]')
        self._default_short_instrument_name = 'alt. trb.'
        self._default_starting_clefs = marktools.ClefMarkInventory([
            marktools.ClefMark('bass'), 
            marktools.ClefMark('tenor'),
            ])

    ### SPECIAL METHODS ###
    def __format__(self, format_specification=''):
        r'''Formats alto trombone.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ..  container:: example

            Without customization:

            ::

                >>> alto_trombone = instrumenttools.AltoTrombone()
                >>> print alto_trombone.storage_format
                instrumenttools.AltoTrombone()

        ..  container:: example

            With customization:

            ::

                >>> custom = instrumenttools.AltoTrombone()
                >>> custom.instrument_name = 'trombone contralto'
                >>> markup = markuptools.Markup('Trombone contralto')
                >>> custom.instrument_name_markup = markup
                >>> custom.short_instrument_name = 'trb. contr.'
                >>> markup = markuptools.Markup('Trb. contr.')
                >>> custom.short_instrument_name_markup = markup
                >>> custom.pitch_range = '[A2, C6]'
                >>> custom.sounding_pitch_of_written_middle_c = 'ef'

            ::

                >>> print custom.storage_format
                instrumenttools.AltoTrombone(
                    instrument_name='trombone contralto',
                    instrument_name_markup=markuptools.Markup((
                        'Trombone contralto',
                        )),
                    short_instrument_name='trb. contr.',
                    short_instrument_name_markup=markuptools.Markup((
                        'Trb. contr.',
                        )),
                    pitch_range=pitchtools.PitchRange(
                        '[A2, C6]'
                        ),
                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch('ef')
                    )

        Returns string.
        '''
        superclass = super(AltoTrombone, self)
        return superclass.__format__(format_specification=format_specification)

    ### PUBLIC PROPERTIES ###

    @apply
    def allowable_clefs():
        def fget(self):
            r'''Gets and sets allowable clefs.

            ..  container:: example

                Gets property:

                ::

                    >>> alto_trombone.allowable_clefs
                    ClefMarkInventory([ClefMark('bass'), ClefMark('tenor')])

                :: 

                    >>> import copy
                    >>> skips = []
                    >>> for clef in alto_trombone.allowable_clefs:
                    ...     skip = scoretools.Skip((1, 8))
                    ...     clef = copy.copy(clef)
                    ...     clef = attach(clef, skip)
                    ...     skips.append(skip)
                    >>> staff = Staff(skips)
                    >>> override(staff).clef.full_size_change = True
                    >>> override(staff).time_signature.stencil = False
                    >>> show(staff) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> alto_trombone.allowable_clefs = ['treble']
                    >>> alto_trombone.allowable_clefs
                    ClefMarkInventory([ClefMark('treble')])

            ..  container:: example

                Restores default:

                ::

                    >>> alto_trombone.allowable_clefs = None
                    >>> alto_trombone.allowable_clefs
                    ClefMarkInventory([ClefMark('bass'), ClefMark('tenor')])

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

                    >>> alto_trombone.instrument_name
                    'alto trombone'

            ..  container:: example

                Sets property:

                ::

                    >>> alto_trombone.instrument_name = 'trombone contralto'
                    >>> alto_trombone.instrument_name
                    'trombone contralto'

            ..  container:: example

                Restores default:

                ::

                    >>> alto_trombone.instrument_name = None
                    >>> alto_trombone.instrument_name
                    'alto trombone'

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

                    >>> alto_trombone.instrument_name_markup
                    Markup(('Alto trombone',))

            ..  container:: example

                Sets property:

                ::

                    >>> markup = markuptools.Markup('Trombone contralto')
                    >>> alto_trombone.instrument_name_markup = markup
                    >>> alto_trombone.instrument_name_markup
                    Markup(('Trombone contralto',))

            ..  container:: example

                Restores default:

                ::

                    >>> alto_trombone.instrument_name_markup = None
                    >>> alto_trombone.instrument_name_markup
                    Markup(('Alto trombone',))

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

                    >>> alto_trombone.pitch_range
                    PitchRange('[A2, Bb5]')

                ::

                    >>> result = scoretools.make_empty_piano_score()
                    >>> score, tenor_staff, bass_staff = result
                    >>> clef = inspect(tenor_staff).get_effective_context_mark(
                    ...     marktools.ClefMark)
                    >>> clef.clef_name = 'tenor'
                    >>> note = Note("c'1")
                    >>> start_pitch = alto_trombone.pitch_range.start_pitch
                    >>> note.written_pitch = start_pitch
                    >>> voice = Voice([note])
                    >>> bass_staff.append(voice)
                    >>> note = Note("c'1")
                    >>> stop_pitch = alto_trombone.pitch_range.stop_pitch
                    >>> note.written_pitch = stop_pitch
                    >>> voice = Voice([note])
                    >>> tenor_staff.append(voice)
                    >>> override(score).time_signature.stencil = False
                    >>> show(score) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> alto_trombone.pitch_range = '[A2, C6]'
                    >>> alto_trombone.pitch_range
                    PitchRange('[A2, C6]')

            ..  container:: example

                Restores default:

                ::

                    >>> alto_trombone.pitch_range = None
                    >>> alto_trombone.pitch_range
                    PitchRange('[A2, Bb5]')

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

                    >>> alto_trombone.short_instrument_name
                    'alt. trb.'
    
            ..  container:: example

                Sets property:

                ::

                    >>> alto_trombone.short_instrument_name = 'trb. contr.'
                    >>> alto_trombone.short_instrument_name
                    'trb. contr.'

            ..  container:: example

                Restores default:

                ::

                    >>> alto_trombone.short_instrument_name = None
                    >>> alto_trombone.short_instrument_name
                    'alt. trb.'

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

                    >>> alto_trombone.short_instrument_name_markup
                    Markup(('Alt. trb.',))

            ..  container:: example

                Sets property:

                ::

                    >>> markup = markuptools.Markup('Trb. contr.')
                    >>> alto_trombone.short_instrument_name_markup = markup
                    >>> alto_trombone.short_instrument_name_markup
                    Markup(('Trb. contr.',))

            ..  container:: example

                Restores default:

                ::

                    >>> alto_trombone.short_instrument_name_markup = None
                    >>> alto_trombone.short_instrument_name_markup
                    Markup(('Alt. trb.',))

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

                    >>> alto_trombone.sounding_pitch_of_written_middle_c
                    NamedPitch("c'")

            ..  container:: example

                Sets property:

                ::

                    >>> alto_trombone.sounding_pitch_of_written_middle_c = 'ef'
                    >>> alto_trombone.sounding_pitch_of_written_middle_c
                    NamedPitch('ef')

            ..  container:: example

                Restores default:

                ::

                    >>> alto_trombone.sounding_pitch_of_written_middle_c = None
                    >>> alto_trombone.sounding_pitch_of_written_middle_c
                    NamedPitch("c'")

            Returns named pitch.
            '''
            return Instrument.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())
