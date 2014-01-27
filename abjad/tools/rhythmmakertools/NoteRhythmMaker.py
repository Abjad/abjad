# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new


class NoteRhythmMaker(RhythmMaker):
    r'''Note rhythm-maker.

    ..  container:: example

        Makes notes equal to the duration of input divisions. Adds ties where
        necessary:

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker()

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> staff = maker._get_rhythmic_staff(lilypond_file)
            >>> f(staff)
            \new RhythmicStaff {
                {
                    \time 5/8
                    c'2 ~
                    c'8
                }
                {
                    \time 3/8
                    c'4.
                }
            }

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _class_name_abbreviation = 'N'

    _human_readable_class_name = 'note rhythm-maker'

    ### INITIALIZER ###

    def __init__(
        self,
        beam_specifier=None,
        duration_spelling_specifier=None,
        tie_specifier=None,
        ):
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            duration_spelling_specifier=duration_spelling_specifier,
            tie_specifier=tie_specifier,
            )

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls note rhythm-maker on `divisions`.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> divisions = [(5, 8), (3, 8)]
                >>> result = maker(divisions)
                >>> for x in result:
                ...     x
                Selection(Note("c'2"), Note("c'8"))
                Selection(Note("c'4."),)

        Returns list of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __eq__(self, arg):
        r'''True when `arg` is a note rhythm-maker with values of
        `beam_specifier`, `duration_spelling_specifier` and `tie_specifier`
        equal to those of this note rhythm-maker. Otherwise false.

        ..  container:: example

            ::

                >>> maker_1 = rhythmmakertools.NoteRhythmMaker()
                >>> tie_specifier = rhythmmakertools.TieSpecifier(
                ...     tie_across_divisions=True,
                ...     )
                >>> maker_2 = rhythmmakertools.NoteRhythmMaker(
                ...     tie_specifier=tie_specifier,
                ...     )

            ::

                >>> maker_1 == maker_1
                True
                >>> maker_1 == maker_2
                False
                >>> maker_2 == maker_1
                False
                >>> maker_2 == maker_2
                True

        Returns boolean.
        '''
        return RhythmMaker.__eq__(self, arg)
        
    def __format__(self, format_specification=''):
        r'''Formats note rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> print format(maker)
                rhythmmakertools.NoteRhythmMaker()

        Returns string.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __illustrate__(self, divisions=None):
        r'''Illustrates note rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> show(maker) # doctest: +SKIP

        Returns LilyPond file.
        '''
        return RhythmMaker.__illustrate__(self, divisions=divisions)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new note rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> tie_specifier = rhythmmakertools.TieSpecifier(
                ...     tie_across_divisions=True,
                ...     )
                >>> new_maker = new(maker, tie_specifier=tie_specifier)

            ::

                >>> print format(new_maker)
                rhythmmakertools.NoteRhythmMaker(
                    tie_specifier=rhythmmakertools.TieSpecifier(
                        tie_across_divisions=True,
                        tie_split_notes=True,
                        ),
                    )

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> music = new_maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = new_maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'2 ~
                        c'8 ~
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns new note rhythm-maker.
        '''
        assert not args
        arguments = {
            'beam_specifier': self.beam_specifier,
            'duration_spelling_specifier': self.duration_spelling_specifier,
            'tie_specifier': self.tie_specifier,
            }
        arguments.update(kwargs)
        maker = type(self)(**arguments)
        return maker

    def __repr__(self):
        r'''Gets interpreter representation of note rhythm-maker.

        ..  container:: example

            ::

                >>> rhythmmakertools.NoteRhythmMaker()
                NoteRhythmMaker()

        Returns string.
        '''
        return RhythmMaker.__repr__(self)

    ### PRIVATE METHODS ###

    def _make_music(self, duration_pairs, seeds):
        from abjad.tools import rhythmmakertools
        selections = []
        specifier = self.duration_spelling_specifier
        if specifier is None:
            specifier = rhythmmakertools.DurationSpellingSpecifier()
        for duration_pair in duration_pairs:
            selection = scoretools.make_leaves(
                pitches=0,
                durations=[duration_pair],
                decrease_durations_monotonically=\
                    specifier.decrease_durations_monotonically,
                forbidden_written_duration=\
                    specifier.forbidden_written_duration,
                )
            selections.append(selection)
        beam_specifier = self.beam_specifier
        if beam_specifier is None:
            beam_specifier = rhythmmakertools.BeamSpecifier()
        if beam_specifier.beam_divisions_together:
            for component in iterate(selections).by_class():
                detach(spannertools.Beam, component)
            beam = spannertools.MultipartBeam()
            leaves = iterate(selections).by_class(scoretools.Leaf)
            leaves = list(leaves)
            attach(beam, leaves) 
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def duration_spelling_specifier(self):
        r'''Gets duration spelling specifier of note rhythm-maker.

        ..  container:: example

            Forbids notes with written duration greater than or equal to 
            ``1/2`` of a whole note:

            ::

                >>> duration_spelling_specifier = \
                ...     rhythmmakertools.DurationSpellingSpecifier(
                ...     forbidden_written_duration=Duration(1, 2),
                ...     )
                >>> maker = rhythmmakertools.NoteRhythmMaker(
                ...     duration_spelling_specifier=duration_spelling_specifier,
                ...     )

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'4 ~
                        c'4 ~
                        c'8
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Returns duration spelling specifier or none.
        '''
        return RhythmMaker.duration_spelling_specifier.fget(self)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses note rhythm-maker.

        ..  container:: example

            ::

                >>> maker = rhythmmakertools.NoteRhythmMaker()
                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.NoteRhythmMaker(
                    duration_spelling_specifier=rhythmmakertools.DurationSpellingSpecifier(
                        decrease_durations_monotonically=False,
                        ),
                    )

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

            ..  doctest::

                >>> staff = maker._get_rhythmic_staff(lilypond_file)
                >>> f(staff)
                \new RhythmicStaff {
                    {
                        \time 5/8
                        c'2 ~
                        c'8
                    }
                    {
                        \time 3/8
                        c'4.
                    }
                }

        Defined equal to copy of note rhythm-maker with
        `duration_spelling_specifier` reversed.

        Returns new note rhythm-maker.
        '''
        from abjad.tools import rhythmmakertools
        duration_spelling_specifier = self.duration_spelling_specifier
        if duration_spelling_specifier is None:
            default = rhythmmakertools.DurationSpellingSpecifier()
            duration_spelling_specifier = default
        duration_spelling_specifier = duration_spelling_specifier.reverse()
        arguments = {
            'duration_spelling_specifier': duration_spelling_specifier,
            }
        result = new(self, **arguments)
        return result
