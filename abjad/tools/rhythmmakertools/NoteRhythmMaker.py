# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.rhythmmakertools.RhythmMaker import RhythmMaker
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import iterate


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

    ..  container:: example

        Forbids notes with written duration greater than or equal to ``1/2``
        of a whole note:

        ::

            >>> maker = rhythmmakertools.NoteRhythmMaker(
            ...     forbidden_written_duration=Duration(1, 2),
            ...     )

        ::

            >>> divisions = [(5, 8), (3, 8)]
            >>> music = maker(divisions)
            >>> lilypond_file = rhythmmakertools.make_lilypond_file(
            ...     music,
            ...     divisions,
            ...     )
            >>> show(lilypond_file) # doctest: +SKIP

    Usage follows the two-step configure-then-call pattern shown here.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    _class_name_abbreviation = 'N'

    _human_readable_class_name = 'note rhythm-maker'

    ### INITIALIZER ###

    # TODO: remove after beam specifier integration into all rhythm-makers
    def __init__(
        self,
        beam_specifier=None,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        tie_across_divisions=False,
        ):
        RhythmMaker.__init__(
            self,
            beam_specifier=beam_specifier,
            decrease_durations_monotonically=decrease_durations_monotonically,
            forbidden_written_duration=forbidden_written_duration,
            tie_across_divisions=tie_across_divisions,
            )

    ### SPECIAL METHODS ###

    def __call__(self, divisions, seeds=None):
        r'''Calls note rhythm-maker on `divisions`.

        Returns list of selections.
        '''
        return RhythmMaker.__call__(
            self,
            divisions,
            seeds=seeds,
            )

    def __format__(self, format_specification=''):
        r'''Formats note rhythm-maker.

        Set `format_specification` to `''` or `'storage'`.

        ..  container:: example

            ::

                >>> print format(maker)
                rhythmmakertools.NoteRhythmMaker(
                    decrease_durations_monotonically=True,
                    forbidden_written_duration=durationtools.Duration(1, 2),
                    tie_across_divisions=False,
                    )

        Returns string.
        '''
        superclass = super(NoteRhythmMaker, self)
        return superclass.__format__(format_specification=format_specification)

    def __makenew__(self, *args, **kwargs):
        r'''Makes new note rhythm-maker.

        ..  container:: example

            ::

                >>> new_maker = new(maker, decrease_durations_monotonically=False)

            ::

                >>> print format(new_maker)
                rhythmmakertools.NoteRhythmMaker(
                    decrease_durations_monotonically=False,
                    forbidden_written_duration=durationtools.Duration(1, 2),
                    tie_across_divisions=False,
                    )

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new note rhythm-maker.
        '''
        #return RhythmMaker.__makenew__(self, *args, **kwargs)
        # TODO: remove after beam specifier integration is complete
        assert not args
        arguments = {
            'beam_specifier': self.beam_specifier,
            'decrease_durations_monotonically':
                self.decrease_durations_monotonically,
            'forbidden_written_duration': self.forbidden_written_duration,
            }
        arguments.update(kwargs)
        maker = type(self)(**arguments)
        return maker

    ### PRIVATE METHODS ###

    def _make_music(self, duration_pairs, seeds):
        from abjad.tools import rhythmmakertools
        selections = []
        for duration_pair in duration_pairs:
            selection = scoretools.make_leaves(
                pitches=0,
                durations=[duration_pair],
                decrease_durations_monotonically=\
                    self.decrease_durations_monotonically,
                forbidden_written_duration=self.forbidden_written_duration,
                )
            selections.append(selection)
        beam_specifier = self.beam_specifier
        if beam_specifier is None:
            beam_specifier = rhythmmakertools.BeamSpecifier()
        if beam_specifier.beam_cells_together:
            for component in iterate(selections).by_class():
                detach(spannertools.Beam, component)
            beam = spannertools.MultipartBeam()
            leaves = iterate(selections).by_class(scoretools.Leaf)
            leaves = list(leaves)
            attach(beam, leaves) 
        return selections

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses note rhythm-maker.

        ..  container:: example

            ::

                >>> reversed_maker = maker.reverse()

            ::

                >>> print format(reversed_maker)
                rhythmmakertools.NoteRhythmMaker(
                    decrease_durations_monotonically=False,
                    forbidden_written_duration=durationtools.Duration(1, 2),
                    tie_across_divisions=False,
                    )

            ::

                >>> divisions = [(5, 8), (3, 8)]
                >>> music = maker(divisions)
                >>> lilypond_file = rhythmmakertools.make_lilypond_file(
                ...     music,
                ...     divisions,
                ...     )
                >>> show(lilypond_file) # doctest: +SKIP

        Returns new note rhythm-maker.
        '''
        return RhythmMaker.reverse(self)
