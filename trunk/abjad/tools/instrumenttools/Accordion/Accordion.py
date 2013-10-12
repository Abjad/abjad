# -*- encoding: utf-8 -*-
from abjad.tools import contexttools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.instrumenttools.Instrument import Instrument


class Accordion(Instrument):
    r'''An accordion.

    ::

        >>> piano_staff = scoretools.PianoStaff()
        >>> piano_staff.append(Staff("c'8 d'8 e'8 f'8"))
        >>> piano_staff.append(Staff("c'4 b4"))
        >>> show(piano_staff) # doctest: +SKIP

    ::

        >>> accordion = instrumenttools.Accordion()
        >>> accordion = accordion.attach(piano_staff)
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
        self._default_instrument_name = 'accordion'
        self._default_performer_names.extend([
            'keyboardist',
            'accordionist',
            ])
        self._default_pitch_range = pitchtools.PitchRange(-32, 48)
        self._default_short_instrument_name = 'acc.'
        self._default_starting_clefs = contexttools.ClefMarkInventory([
            contexttools.ClefMark('treble'), 
            contexttools.ClefMark('bass'),
            ])
        self._is_primary_instrument = True
        self._copy_default_starting_clefs_to_default_allowable_clefs()

    ### PRIVATE PROPERTIES ###

    # TODO: extend class definition to allow for custom target context in repr
    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        return ()

    ### PUBLIC PROPERTIES ###

    @apply
    def allowable_clefs():
        def fget(self):
            r'''Gets and sets allowable clefs.

            ::

                >>> accordion.allowable_clefs
                ClefMarkInventory([ClefMark('treble'), ClefMark('bass')])

            ::

                >>> import copy
                >>> skips = []
                >>> for clef in accordion.allowable_clefs:
                ...     skip = skiptools.Skip((1, 8))
                ...     clef = copy.copy(clef)
                ...     clef = clef.attach(skip)
                ...     skips.append(skip)
                >>> staff = Staff(skips)
                >>> staff.override.clef.full_size_change = True
                >>> staff.override.time_signature.stencil = False
                >>> show(staff) # doctest: +SKIP

            ::

                >>> accordion.allowable_clefs = ['treble']
                >>> accordion.allowable_clefs
                ClefMarkInventory([ClefMark('treble')])

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

            ::

                >>> accordion.instrument_name
                'accordion'

            ::

                >>> accordion.instrument_name = 'fisarmonica'
                >>> accordion.instrument_name
                'fisarmonica'

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

            ::

                >>> accordion.instrument_name_markup
                Markup(('Accordion',))

            ::

                >>> markup = markuptools.Markup('fisarmonica')
                >>> accordion.instrument_name_markup = markup
                >>> accordion.instrument_name_markup
                Markup(('fisarmonica',))

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
            r'''Gets and sets pitch range.

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
                >>> show(score) # doctest: +SKIP

            ::

                >>> accordion.pitch_range = '[C2, C6]'
                >>> accordion.pitch_range
                PitchRange('[C2, C6]')

            ::

                >>> accordion.pitch_range = None
                >>> accordion.pitch_range
                PitchRange('[E1, C8]')

            Returns pitch range.
            '''
            return Instrument.pitch_range.fget(self)
        def fset(self, pitch_range):
            Instrument.pitch_range.fset(self, pitch_range)
        return property(**locals())

    @apply
    def short_instrument_name():
        def fget(self):
            r'''Gets and sets short instrument name.

            ::

                >>> accordion.short_instrument_name
                'acc.'
    
            ::

                >>> accordion.short_instrument_name = 'fis.'
                >>> accordion.short_instrument_name
                'fis.'

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

            ::

                >>> accordion.short_instrument_name_markup
                Markup(('Acc.',))

            ::

                >>> markup = markuptools.Markup('fis.')
                >>> accordion.short_instrument_name_markup = markup
                >>> accordion.short_instrument_name_markup
                Markup(('fis.',))

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

            ::

                >>> accordion.sounding_pitch_of_written_middle_c
                NamedPitch("c'")

            ::

                >>> pitch = accordion.sounding_pitch_of_written_middle_c
                >>> note = Note(pitch, Duration(1))
                >>> staff = Staff([note])
                >>> staff.override.time_signature.stencil = False
                >>> show(staff) # doctest: +SKIP

            ::

                >>> accordion.sounding_pitch_of_written_middle_c = 'cs'
                >>> accordion.sounding_pitch_of_written_middle_c
                NamedPitch('cs')

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
