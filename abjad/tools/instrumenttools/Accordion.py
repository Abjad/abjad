# -*- encoding: utf-8 -*-
from abjad.tools import marktools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


class Accordion(Instrument):
    r'''An accordion.

    ::

        >>> piano_staff = scoretools.PianoStaff()
        >>> piano_staff.append(Staff("c'8 d'8 e'8 f'8"))
        >>> piano_staff.append(Staff("c'4 b4"))
        >>> accordion = instrumenttools.Accordion()
        >>> accordion = attach(accordion, piano_staff)
        >>> show(piano_staff) # doctest: +SKIP

    ..  doctest::

        >>> f(piano_staff)
        \new PianoStaff <<
            \set PianoStaff.instrumentName = \markup { Accordion }
            \set PianoStaff.shortInstrumentName = \markup { Acc. }
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'4
                b4
            }
        >>

    The accordion targets the piano staff context by default.
    '''

    ### INITIALIZER ###

    def __init__(self, target_context=None, **kwargs):
        if target_context is None:
            target_context = scoretools.PianoStaff
        Instrument.__init__(
            self, 
            target_context=target_context, 
            **kwargs
            )
        self._default_allowable_clefs = marktools.ClefMarkInventory([
            marktools.ClefMark('treble'), 
            marktools.ClefMark('bass'),
            ])
        self._default_instrument_name = 'accordion'
        self._default_performer_names.extend([
            'keyboardist',
            'accordionist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(-32, 48)
        self._default_short_instrument_name = 'acc.'
        self._default_starting_clefs = marktools.ClefMarkInventory([
            marktools.ClefMark('treble'), 
            marktools.ClefMark('bass'),
            ])
        self._is_primary_instrument = True

    ### PUBLIC PROPERTIES ###

    @apply
    def allowable_clefs():
        def fget(self):
            r'''Gets and sets allowable clefs.

            ..  container:: example

                Gets property:

                ::

                    >>> accordion.allowable_clefs
                    ClefMarkInventory([ClefMark('treble'), ClefMark('bass')])

                ::

                    >>> import copy
                    >>> skips = []
                    >>> for clef in accordion.allowable_clefs:
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

                    >>> accordion.allowable_clefs = ['treble']
                    >>> accordion.allowable_clefs
                    ClefMarkInventory([ClefMark('treble')])

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.allowable_clefs = None
                    >>> accordion.allowable_clefs
                    ClefMarkInventory([ClefMark('treble'), ClefMark('bass')])

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

                    >>> accordion.instrument_name
                    'accordion'

            ..  container:: example

                Sets property:

                ::

                    >>> accordion.instrument_name = 'fisarmonica'
                    >>> accordion.instrument_name
                    'fisarmonica'

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.instrument_name = None
                    >>> accordion.instrument_name
                    'accordion'

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

                    >>> accordion.instrument_name_markup
                    Markup(('Accordion',))

            ..  container:: example

                Sets property:

                ::

                    >>> markup = markuptools.Markup('Fisarmonica')
                    >>> accordion.instrument_name_markup = markup
                    >>> accordion.instrument_name_markup
                    Markup(('Fisarmonica',))

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.instrument_name_markup = None
                    >>> accordion.instrument_name_markup
                    Markup(('Accordion',))

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

                    >>> accordion.pitch_range
                    PitchRange('[E1, C8]')

                ::

                    >>> result = scoretools.make_empty_piano_score()
                    >>> score, treble_staff, bass_staff = result
                    >>> note = Note("c'1")
                    >>> note.written_pitch = accordion.pitch_range.start_pitch
                    >>> bass_staff.append(note)
                    >>> note = Note("c'1")
                    >>> note.written_pitch = accordion.pitch_range.stop_pitch
                    >>> treble_staff.append(note)
                    >>> override(score).time_signature.stencil = False
                    >>> show(score) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> accordion.pitch_range = '[C2, C6]'
                    >>> accordion.pitch_range
                    PitchRange('[C2, C6]')

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.pitch_range = None
                    >>> accordion.pitch_range
                    PitchRange('[E1, C8]')

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

                    >>> accordion.short_instrument_name
                    'acc.'

            ..  container:: example

                Sets property:
        
                ::

                    >>> accordion.short_instrument_name = 'fis.'
                    >>> accordion.short_instrument_name
                    'fis.'

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.short_instrument_name = None
                    >>> accordion.short_instrument_name
                    'acc.'

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

                    >>> accordion.short_instrument_name_markup
                    Markup(('Acc.',))

            ..  container:: example

                Sets property:

                ::

                    >>> markup = markuptools.Markup('fis.')
                    >>> accordion.short_instrument_name_markup = markup
                    >>> accordion.short_instrument_name_markup
                    Markup(('fis.',))

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.short_instrument_name_markup = None
                    >>> accordion.short_instrument_name_markup
                    Markup(('Acc.',))

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

                    >>> accordion.sounding_pitch_of_written_middle_c
                    NamedPitch("c'")

                ::

                    >>> pitch = accordion.sounding_pitch_of_written_middle_c
                    >>> note = Note(pitch, Duration(1))
                    >>> staff = Staff([note])
                    >>> override(staff).time_signature.stencil = False
                    >>> show(staff) # doctest: +SKIP

            ..  container:: example

                Sets property:

                ::

                    >>> accordion.sounding_pitch_of_written_middle_c = 'cs'
                    >>> accordion.sounding_pitch_of_written_middle_c
                    NamedPitch('cs')

            ..  container:: example

                Restores default:

                ::

                    >>> accordion.sounding_pitch_of_written_middle_c = None
                    >>> accordion.sounding_pitch_of_written_middle_c
                    NamedPitch("c'")

            Returns named pitch.
            '''
            return Instrument.sounding_pitch_of_written_middle_c.fget(self)
        def fset(self, pitch):
            Instrument.sounding_pitch_of_written_middle_c.fset(self, pitch)
        return property(**locals())

    @property
    def storage_format(self):
        r'''Accordion storage format.

        ..  container:: example

            Without customization:

            ::

                >>> accordion = instrumenttools.Accordion()
                >>> print accordion.storage_format
                instrumenttools.Accordion()

        ..  container:: example

            With customization:

            ::

                >>> custom = instrumenttools.Accordion()
                >>> custom.instrument_name = 'fisarmonica'
                >>> markup = markuptools.Markup('Fisarmonica')
                >>> custom.instrument_name_markup = markup
                >>> custom.short_instrument_name = 'fis.'
                >>> markup = markuptools.Markup('Fis.')
                >>> custom.short_instrument_name_markup = markup
                >>> custom.allowable_clefs = ['treble']
                >>> custom.pitch_range = '[C4, C6]'
                >>> custom.sounding_pitch_of_written_middle_c = "c''"

            ::

                >>> print custom.storage_format
                instrumenttools.Accordion(
                    instrument_name='fisarmonica',
                    instrument_name_markup=markuptools.Markup((
                        'Fisarmonica',
                        )),
                    short_instrument_name='fis.',
                    short_instrument_name_markup=markuptools.Markup((
                        'Fis.',
                        )),
                    allowable_clefs=marktools.ClefMarkInventory([
                        marktools.ClefMark(
                            'treble',
                            target_context=scoretools.Staff
                            ),
                        ]),
                    pitch_range=pitchtools.PitchRange(
                        '[C4, C6]'
                        ),
                    sounding_pitch_of_written_middle_c=pitchtools.NamedPitch("c''")
                    )

        Returns string.
        '''
        superclass = super(Accordion, self)
        return superclass.storage_format
