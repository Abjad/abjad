# -*- coding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


class TempoList(TypedList):
    r'''Tempo list.

    ..  container:: example

        ::

            >>> tempos = indicatortools.TempoList([
            ...     (Duration(1, 8), 72, 'Andante'),
            ...     (Duration(1, 8), 84, 'Allegro'),
            ...     ])

        ::

            >>> for tempo in tempos:
            ...     tempo
            ...
            Tempo(reference_duration=Duration(1, 8), units_per_minute=72, textual_indication='Andante')
            Tempo(reference_duration=Duration(1, 8), units_per_minute=84, textual_indication='Allegro')

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collections'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when tempo list contains `argument`.

        ..  container:: example

            ::

                >>> tempos = indicatortools.TempoList([
                ...     (Duration(1, 8), 72),
                ...     ((1, 8), 84, 'Allegro'),
                ...     ])

            ::

                >>> Tempo((1, 8), 72) in tempos
                True

            ::

                >>> ((1, 8), 72) in tempos
                True

            ::

                >>> (Duration(1, 8), 72) in tempos
                True

            ::

                >>> ((1, 8), 84, 'Allegro') in tempos
                True

            ::

                >>> ((1, 8), 96) in tempos
                False

        Returns true or false.
        '''
        superclass = super(TempoList, self)
        return superclass.__contains__(argument)

    def __format__(self, format_specification=''):
        r'''Formats tempo list.

        ..  container:: example

            ::

                >>> tempos = indicatortools.TempoList([
                ...     (Duration(1, 8), 72),
                ...     ((1, 8), 84, 'Allegro'),
                ...     ])

            ::

                >>> f(tempos)
                indicatortools.TempoList(
                    [
                        indicatortools.Tempo(
                            reference_duration=durationtools.Duration(1, 8),
                            units_per_minute=72,
                            ),
                        indicatortools.Tempo(
                            reference_duration=durationtools.Duration(1, 8),
                            units_per_minute=84,
                            textual_indication='Allegro',
                            ),
                        ]
                    )

        Returns string.
        '''
        superclass = super(TempoList, self)
        return superclass.__format__(format_specification=format_specification)

    def __illustrate__(self):
        r'''Illustrates tempos.

        ..  container:: example

            ::

                >>> tempos = indicatortools.TempoList([
                ...     (Duration(1, 8), 72),
                ...     ((1, 8), 84, 'Allegro'),
                ...     ])

            ::

                >>> show(tempos) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = tempos.__illustrate__()
                >>> f(lilypond_file[Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Clef.stencil = ##f
                    \override NoteHead.no-ledgers = ##t
                    \override NoteHead.transparent = ##t
                    \override StaffSymbol.transparent = ##t
                    \override Stem.transparent = ##t
                    \override TimeSignature.stencil = ##f
                } <<
                    \new Staff {
                        \time 2/4
                        \break
                        c'2
                        \tempo 8=72
                        \break
                        c'2
                        \tempo Allegro 8=84
                        \break
                        c'2
                    }
                >>

        Returns LilyPond file.
        '''
        import abjad
        staff = abjad.Staff()
        score = abjad.Score([staff])
        time_signature = abjad.TimeSignature((2, 4))
        abjad.attach(time_signature, staff)
        # the zero note avoids a lilypond spacing problem:
        # score-initial tempo indications slip to the left
        zero_note = abjad.Note("c'2")
        staff.append(zero_note)
        command = abjad.LilyPondCommand('break')
        abjad.attach(command, zero_note)
        for tempo in self.items:
            note = abjad.Note("c'2")
            abjad.attach(tempo, note)
            staff.append(note)
            command = abjad.LilyPondCommand('break')
            abjad.attach(command, note)
        abjad.override(score).bar_line.transparent = True
        abjad.override(score).bar_number.stencil = False
        abjad.override(score).clef.stencil = False
        abjad.override(score).note_head.no_ledgers = True
        abjad.override(score).note_head.transparent = True
        abjad.override(score).staff_symbol.transparent = True
        abjad.override(score).stem.transparent = True
        abjad.override(score).time_signature.stencil = False
        lilypond_file = abjad.LilyPondFile.new(score)
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        lilypond_file.items.remove(lilypond_file['paper'])
        lilypond_file.header_block.tagline = False
        return lilypond_file

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        def coerce_(argument):
            if argument is None:
                tempo = indicatortools.Tempo()
            elif isinstance(argument, tuple):
                tempo = indicatortools.Tempo(*argument)
            elif isinstance(argument, indicatortools.Tempo):
                tempo = copy.copy(argument)
            else:
                raise TypeError(repr(argument))
            return tempo
        from abjad.tools import indicatortools
        return coerce_

    ### PUBLIC ###

    def append(self, tempo):
        r'''Appends tempo.

        ..  container:: example

            ::

                >>> tempos_1 = indicatortools.TempoList([((1, 8), 72)])
                >>> tempos_1.append(((1, 8), 84))
                >>> tempos_2 = indicatortools.TempoList([
                ...    ((1, 8), 72),
                ...    ((1, 8), 84),
                ...    ])

            ::

                >>> tempos_1 == tempos_2
                True

        Returns none.
        '''
        superclass = super(TempoList, self)
        return superclass.append(tempo)
