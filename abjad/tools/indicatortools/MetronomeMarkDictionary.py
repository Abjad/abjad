import copy
from abjad.tools.datastructuretools.TypedOrderedDict import TypedOrderedDict


class MetronomeMarkDictionary(TypedOrderedDict):
    r'''Metronome mark dictionary.

    ..  container:: example

        >>> marks = abjad.MetronomeMarkDictionary([
        ...     ('andante', ((1, 8), 72, 'Andante')),
        ...     ('allegro', ((1, 8), 84, 'Allegro')),
        ...     ])

        >>> for name in marks:
        ...     marks[name]
        ...
        MetronomeMark(reference_duration=Duration(1, 8), units_per_minute=72, textual_indication='Andante')
        MetronomeMark(reference_duration=Duration(1, 8), units_per_minute=84, textual_indication='Allegro')

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Collections'

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats metronome mark dictionary.

        ..  container:: example

            >>> marks = abjad.MetronomeMarkDictionary([
            ...     ('andante', ((1, 8), 72, 'Andante')),
            ...     ('allegro', ((1, 8), 84, 'Allegro')),
            ...     ])

            >>> abjad.f(marks)
            abjad.MetronomeMarkDictionary(
                [
                    (
                        'andante',
                        abjad.MetronomeMark(
                            reference_duration=abjad.Duration(1, 8),
                            units_per_minute=72,
                            textual_indication='Andante',
                            ),
                        ),
                    (
                        'allegro',
                        abjad.MetronomeMark(
                            reference_duration=abjad.Duration(1, 8),
                            units_per_minute=84,
                            textual_indication='Allegro',
                            ),
                        ),
                    ]
                )

        Returns string.
        '''
        superclass = super(MetronomeMarkDictionary, self)
        return superclass.__format__(format_specification=format_specification)

    def __illustrate__(self):
        r'''Illustrates marks.

        ..  container:: example

            >>> marks = abjad.MetronomeMarkDictionary([
            ...     ('andante', ((1, 8), 72, 'Andante')),
            ...     ('allegro', ((1, 8), 84, 'Allegro')),
            ...     ])

            >>> abjad.show(marks) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = marks.__illustrate__()
                >>> abjad.f(lilypond_file[abjad.Score])
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
                        \tempo Andante 8=72
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
        for name, mark in self.items():
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

    ### PRIVATE METHODS ###

    @staticmethod
    def _item_coercer(argument):
        import abjad
        if argument is None:
            mark = abjad.MetronomeMark()
        elif isinstance(argument, tuple):
            mark = abjad.MetronomeMark(*argument)
        elif isinstance(argument, abjad.MetronomeMark):
            mark = copy.copy(argument)
        else:
            raise TypeError(repr(argument))
        return mark
