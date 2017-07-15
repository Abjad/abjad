# -*- coding: utf-8 -*-
import copy
from abjad.tools.datastructuretools.TypedList import TypedList


class MetronomeMarkList(TypedList):
    r'''Metronome mark list.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> marks = abjad.MetronomeMarkList([
            ...     ((1, 8), 72, 'Andante'),
            ...     ((1, 8), 84, 'Allegro'),
            ...     ])

        ::

            >>> for mark in marks:
            ...     mark
            ...
            MetronomeMark(reference_duration=Duration(1, 8), units_per_minute=72, textual_indication='Andante')
            MetronomeMark(reference_duration=Duration(1, 8), units_per_minute=84, textual_indication='Allegro')

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collections'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        r'''Is true when metronome mark list contains `argument`.

        ..  container:: example

            ::

                >>> marks = abjad.MetronomeMarkList([
                ...     (abjad.Duration(1, 8), 72),
                ...     ((1, 8), 84, 'Allegro'),
                ...     ])

            ::

                >>> abjad.MetronomeMark((1, 8), 72) in marks
                True

            ::

                >>> ((1, 8), 72) in marks
                True

            ::

                >>> (abjad.Duration(1, 8), 72) in marks
                True

            ::

                >>> ((1, 8), 84, 'Allegro') in marks
                True

            ::

                >>> ((1, 8), 96) in marks
                False

        Returns true or false.
        '''
        superclass = super(MetronomeMarkList, self)
        return superclass.__contains__(argument)

    def __format__(self, format_specification=''):
        r'''Formats metronome mark list.

        ..  container:: example

            ::

                >>> marks = abjad.MetronomeMarkList([
                ...     (abjad.Duration(1, 8), 72),
                ...     ((1, 8), 84, 'Allegro'),
                ...     ])

            ::

                >>> f(marks)
                abjad.MetronomeMarkList(
                    [
                        abjad.MetronomeMark(
                            reference_duration=abjad.Duration(1, 8),
                            units_per_minute=72,
                            ),
                        abjad.MetronomeMark(
                            reference_duration=abjad.Duration(1, 8),
                            units_per_minute=84,
                            textual_indication='Allegro',
                            ),
                        ]
                    )

        Returns string.
        '''
        superclass = super(MetronomeMarkList, self)
        return superclass.__format__(format_specification=format_specification)

    def __illustrate__(self):
        r'''Illustrates marks.

        ..  container:: example

            ::

                >>> marks = abjad.MetronomeMarkList([
                ...     (abjad.Duration(1, 8), 72),
                ...     ((1, 8), 84, 'Allegro'),
                ...     ])

            ::

                >>> show(marks) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = marks.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
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
        # the zero note avoids a lilypond spacing problem:
        # score-initial metronome marks slip to the left
        zero_note = abjad.Note("c'2")
        staff.append(zero_note)
        command = abjad.LilyPondCommand('break')
        abjad.attach(command, zero_note)
        for mark in self.items:
            note = abjad.Note("c'2")
            abjad.attach(mark, note)
            staff.append(note)
            command = abjad.LilyPondCommand('break')
            abjad.attach(command, note)
        leaf = abjad.inspect(staff).get_leaf(0)
        time_signature = abjad.TimeSignature((2, 4))
        abjad.attach(time_signature, leaf)
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
                mark = indicatortools.MetronomeMark()
            elif isinstance(argument, tuple):
                mark = indicatortools.MetronomeMark(*argument)
            elif isinstance(argument, indicatortools.MetronomeMark):
                mark = copy.copy(argument)
            else:
                raise TypeError(repr(argument))
            return mark
        from abjad.tools import indicatortools
        return coerce_

    ### PUBLIC ###

    def append(self, mark):
        r'''Appends metronome `mark`.

        ..  container:: example

            ::

                >>> marks_1 = abjad.MetronomeMarkList([((1, 8), 72)])
                >>> marks_1.append(((1, 8), 84))
                >>> marks_2 = abjad.MetronomeMarkList([
                ...    ((1, 8), 72),
                ...    ((1, 8), 84),
                ...    ])

            ::

                >>> marks_1 == marks_2
                True

        Returns none.
        '''
        superclass = super(MetronomeMarkList, self)
        return superclass.append(mark)
