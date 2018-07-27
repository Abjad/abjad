import copy
from .Context import Context


class Score(Context):
    r"""
    Score.

    ..  container:: example

        >>> staff_1 = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> staff_2 = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> score = abjad.Score([staff_1, staff_2])
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
                \new Staff
                {
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Contexts'

    __slots__ = ()

    _default_lilypond_type = 'Score'

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        lilypond_type='Score',
        is_simultaneous=True,
        name=None,
        ):
        Context.__init__(
            self,
            components=components,
            lilypond_type=lilypond_type,
            is_simultaneous=is_simultaneous,
            name=name,
            )

    ### PUBLIC METHODS ###

    def add_final_bar_line(
        self,
        abbreviation='|.',
        to_each_voice=False,
        ):
        r"""
        Add final bar line to end of score.


            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> score = abjad.Score([staff])
            >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>


        >>> bar_line = score.add_final_bar_line()
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            <<
                \new Staff
                {
                    c'4
                    d'4
                    e'4
                    f'4
                    \bar "|." %! SCORE1
                }
            >>

        Set ``to_each_voice`` to true to make part extraction easier.

        Returns bar line.
        """
        import abjad
        bar_line = abjad.BarLine(abbreviation)
        if not to_each_voice:
            last_leaf = abjad.inspect(self).leaf(-1)
            abjad.attach(bar_line, last_leaf, tag='SCORE1')
        else:
            for voice in abjad.iterate(self).components(abjad.Voice):
                last_leaf = abjad.inspect(voice).leaf(-1)
                abjad.attach(bar_line, last_leaf, tag='SCORE1')
        return bar_line

    def add_final_markup(self, markup, extra_offset=None):
        r"""
        Adds ``markup`` to end of score.

        ..  container:: example

            Adds markup to last leaf:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> score = abjad.Score([staff])
            >>> place = abjad.Markup('Bremen - Boston - LA.', direction=abjad.Down)
            >>> date = abjad.Markup('July 2010 - May 2011.')
            >>> markup = abjad.Markup.right_column([place, date], direction=abjad.Down)
            >>> markup = markup.italic()
            >>> markup = score.add_final_markup(
            ...     markup,
            ...     extra_offset=(0.5, -2),
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    {
                        c'4
                        d'4
                        e'4
                        \once \override TextScript.extra-offset = #'(0.5 . -2)
                        f'4
                        _ \markup { %! SCORE2
                            \italic %! SCORE2
                                \right-column %! SCORE2
                                    { %! SCORE2
                                        "Bremen - Boston - LA." %! SCORE2
                                        "July 2010 - May 2011." %! SCORE2
                                    } %! SCORE2
                            } %! SCORE2
                    }
                >>

        ..  container:: example

            Adds markup to last multimeasure rest:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> staff.append(abjad.MultimeasureRest((4, 4)))
            >>> score = abjad.Score([staff])
            >>> place = abjad.Markup(
            ...     'Bremen - Boston - LA.',
            ...     direction=abjad.Down,
            ...     )
            >>> date = abjad.Markup('July 2010 - May 2011.')
            >>> markup = abjad.Markup.right_column(
            ...     [place, date],
            ...     direction=abjad.Down,
            ...     )
            >>> markup = markup.italic()
            >>> markup = score.add_final_markup(
            ...     markup,
            ...     extra_offset=(14.5, -2),
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(score)
                \new Score
                <<
                    \new Staff
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \once \override MultiMeasureRestText.extra-offset = #'(14.5 . -2)
                        R1
                        _ \markup { %! SCORE2
                            \italic %! SCORE2
                                \right-column %! SCORE2
                                    { %! SCORE2
                                        "Bremen - Boston - LA." %! SCORE2
                                        "July 2010 - May 2011." %! SCORE2
                                    } %! SCORE2
                            } %! SCORE2
                    }
                >>

        Returns none.
        """
        import abjad
        selection = abjad.select(self)
        last_leaf = selection._get_component(abjad.Leaf, -1)
        markup = copy.copy(markup)
        abjad.attach(markup, last_leaf, tag='SCORE2')
        if extra_offset is not None:
            if isinstance(last_leaf, abjad.MultimeasureRest):
                grob_proxy = abjad.override(last_leaf).multi_measure_rest_text
            else:
                grob_proxy = abjad.override(last_leaf).text_script
            grob_proxy.extra_offset = extra_offset
        return markup

    @staticmethod
    def make_piano_score(leaves=None, lowest_treble_pitch='B3', sketch=False):
        r"""
        Makes piano score from ``leaves``.

        ..  container:: example

            Makes empty piano score:

            >>> result = abjad.Score.make_piano_score()

            >>> abjad.f(result[0])
            \new Score
            <<
                \new PianoStaff
                <<
                    \context Staff = "Treble Staff"
                    {
                    }
                    \context Staff = "Bass Staff"
                    {
                    }
                >>
            >>

        ..  container:: example

            Makes piano score from leaves:

            >>> notes = [abjad.Note(x, (1, 4)) for x in [-12, 37, -10, 2, 4, 17]]
            >>> result = abjad.Score.make_piano_score(leaves=notes)
            >>> abjad.show(result[0]) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(result[0])
                \new Score
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
                        {
                            \clef "treble"
                            r4
                            cs''''4
                            r4
                            d'4
                            e'4
                            f''4
                        }
                        \context Staff = "Bass Staff"
                        {
                            \clef "bass"
                            c4
                            r4
                            d4
                            r4
                            r4
                            r4
                        }
                    >>
                >>

        ..  container:: example

            Makes piano sketch score from leaves:

            >>> maker = abjad.NoteMaker()
            >>> notes = maker(
            ...     [-12, -10, -8, -7, -5, 0, 2, 4, 5, 7],
            ...     [(1, 16)],
            ...     )
            >>> result = abjad.Score.make_piano_score(
            ...     leaves=notes,
            ...     sketch=True,
            ...     )
            >>> abjad.show(result[0]) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(result[0])
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
                        {
                            \clef "treble"
                            r16
                            r16
                            r16
                            r16
                            r16
                            c'16
                            d'16
                            e'16
                            f'16
                            g'16
                        }
                        \context Staff = "Bass Staff"
                        {
                            \clef "bass"
                            c16
                            d16
                            e16
                            f16
                            g16
                            r16
                            r16
                            r16
                            r16
                            r16
                        }
                    >>
                >>


        Returns score, treble staff, bass staff triple.
        """
        import abjad
        leaves = leaves or []
        lowest_treble_pitch = abjad.NamedPitch(lowest_treble_pitch)
        treble_staff = abjad.Staff(name='Treble Staff')
        bass_staff = abjad.Staff(name='Bass Staff')
        staff_group = abjad.StaffGroup(
            [treble_staff, bass_staff],
            lilypond_type='PianoStaff',
            )
        score = abjad.Score()
        score.append(staff_group)
        for leaf in leaves:
            treble_pitches, bass_pitches = [], []
            for pitch in abjad.inspect(leaf).pitches():
                if pitch < lowest_treble_pitch:
                    bass_pitches.append(pitch)
                else:
                    treble_pitches.append(pitch)
            written_duration = leaf.written_duration
            if not treble_pitches:
                treble_leaf = abjad.Rest(written_duration)
            elif len(treble_pitches) == 1:
                treble_leaf = abjad.Note(treble_pitches[0], written_duration)
            else:
                treble_leaf = abjad.Chord(treble_pitches, written_duration)
            treble_staff.append(treble_leaf)
            if not bass_pitches:
                bass_leaf = abjad.Rest(written_duration)
            elif len(bass_pitches) == 1:
                bass_leaf = abjad.Note(bass_pitches[0], written_duration)
            else:
                bass_leaf = abjad.Chord(bass_pitches, written_duration)
            bass_staff.append(bass_leaf)
        if 0 < len(treble_staff):
            abjad.attach(abjad.Clef('treble'), treble_staff[0])
        if 0 < len(bass_staff):
            abjad.attach(abjad.Clef('bass'), bass_staff[0])
        if sketch:
            abjad.override(score).time_signature.stencil = False
            abjad.override(score).bar_number.transparent = True
            abjad.override(score).bar_line.stencil = False
            abjad.override(score).span_bar.stencil = False
        return score, treble_staff, bass_staff
