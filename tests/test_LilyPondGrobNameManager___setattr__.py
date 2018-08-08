import abjad
import pytest


def test_LilyPondGrobNameManager___setattr___01():
    """
    Override LilyPond Accidental grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).accidental.color = 'red'

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override Accidental.color = #red
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___02():
    """
    Override LilyPond Accidental grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff[1]).accidental.color = 'red'

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            \once \override Accidental.color = #red
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___03():
    """
    Override LilyPond BarNumber grob.
    """

    score = abjad.Score([abjad.Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")])
    abjad.override(score).bar_number.break_visibility = \
        abjad.Scheme('end-of-line-invisible')

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            \override BarNumber.break-visibility = #end-of-line-invisible
        }
        <<
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
                g'8
                a'8
                b'8
                c''8
            }
        >>
        """
        )
    assert abjad.inspect(score).is_wellformed()


def test_LilyPondGrobNameManager___setattr___04():
    """
    Override LilyPond BarNumber grob.
    """

    score = abjad.Score([abjad.Staff("c'8 d'8 e'8 f'8")])
    abjad.override(score).bar_number.color = 'red'

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            \override BarNumber.color = #red
        }
        <<
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
        )

    assert abjad.inspect(score).is_wellformed()


def test_LilyPondGrobNameManager___setattr___05():
    """
    Override LilyPond abjad.Clef grob.
    """

    note = abjad.Note("c'4")
    abjad.override(note).clef.color = 'red'

    assert format(note) == abjad.String.normalize(
        r"""
        \once \override Clef.color = #red
        c'4
        """
        )


def test_LilyPondGrobNameManager___setattr___06():
    """
    Override LilyPond abjad.Clef grob.
    """

    note = abjad.Note("c'4")
    abjad.override(note).staff.clef.color = 'red'

    assert format(note) == abjad.String.normalize(
        r"""
        \once \override Staff.Clef.color = #red
        c'4
        """
        )


def test_LilyPondGrobNameManager___setattr___07():
    """
    Override LilyPond abjad.Clef grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).clef.color = 'red'

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override Clef.color = #red
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___08():
    """
    Override LilyPond ClusterSpanner grob.
    """

    cluster = abjad.Cluster(abjad.Note(1, (1, 4)) * 4)
    abjad.override(cluster).cluster_spanner.style = 'ramp'
    abjad.override(cluster).cluster_spanner.padding = 0.1

    assert format(cluster) == abjad.String.normalize(
        r"""
        \makeClusters {
            \override ClusterSpanner.padding = #0.1
            \override ClusterSpanner.style = #'ramp
            cs'4
            cs'4
            cs'4
            cs'4
            \revert ClusterSpanner.padding
            \revert ClusterSpanner.style
        }
        """
        )

    del(abjad.override(cluster).cluster_spanner)

    assert format(cluster) == abjad.String.normalize(
        r"""
        \makeClusters {
            cs'4
            cs'4
            cs'4
            cs'4
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___09():
    """
    Override LilyPond abjad.DynamicLineSpanner grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).dynamic_line_spanner.staff_padding = 2
    abjad.override(staff).dynamic_line_spanner.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override DynamicLineSpanner.Y-extent = #'(-1.5 . 1.5)
            \override DynamicLineSpanner.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___10():
    """
    Override LilyPond abjad.DynamicText grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).dynamic_text.staff_padding = 2
    abjad.override(staff).dynamic_text.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override DynamicText.Y-extent = #'(-1.5 . 1.5)
            \override DynamicText.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___11():
    """
    Override LilyPond abjad.DynamicTextSpanner grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).dynamic_text_spanner.staff_padding = 2
    abjad.override(staff).dynamic_text_spanner.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override DynamicTextSpanner.Y-extent = #'(-1.5 . 1.5)
            \override DynamicTextSpanner.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___12():
    """
    Override LilyPond Hairpin grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).hairpin.staff_padding = 2
    abjad.override(staff).hairpin.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override Hairpin.Y-extent = #'(-1.5 . 1.5)
            \override Hairpin.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___13():
    """
    Override LilyPond InstrumentName grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.setting(staff).instrument_name = abjad.Markup(r'\circle { V }')
    abjad.override(staff).instrument_name.color = 'red'

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override InstrumentName.color = #red
            instrumentName = \markup {
                \circle
                    {
                        V
                    }
                }
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )

    assert abjad.inspect(staff).is_wellformed()


def test_LilyPondGrobNameManager___setattr___14():
    """
    Override LilyPond abjad.MetronomeMark grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    score = abjad.Score([staff])
    tempo = abjad.MetronomeMark(abjad.Duration(1, 4), 58)
    abjad.attach(tempo, staff[0])
    abjad.override(score).metronome_mark.color = 'red'

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            \override MetronomeMark.color = #red
        }
        <<
            \new Staff
            {
                \tempo 4=58
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
        )

    assert abjad.inspect(score).is_wellformed()


def test_LilyPondGrobNameManager___setattr___15():
    """
    Override LilyPond MultiMeasureRestGrob.
    """

    staff = abjad.Staff([abjad.Note("c'4")])
    abjad.override(staff).multi_measure_rest.expand_limit = 12

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override MultiMeasureRest.expand-limit = #12
        }
        {
            c'4
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___16():
    """
    Override LilyPond NonMusicalPaperColumn grob.
    """

    score = abjad.Score([abjad.Staff("c'8 d'8 e'8 f'8")])
    abjad.override(score).non_musical_paper_column.line_break_permission = False
    abjad.override(score).non_musical_paper_column.page_break_permission = False

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            \override NonMusicalPaperColumn.line-break-permission = ##f
            \override NonMusicalPaperColumn.page-break-permission = ##f
        }
        <<
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
        )

    assert abjad.inspect(score).is_wellformed()


def test_LilyPondGrobNameManager___setattr___17():
    """
    Override LilyPond abjad.NoteColumn grob.
    """

    note = abjad.Note("c'4")
    abjad.override(note).note_column.ignore_collision = True

    assert format(note) == abjad.String.normalize(
        r"""
        \once \override NoteColumn.ignore-collision = ##t
        c'4
        """
        )

    assert abjad.inspect(note).is_wellformed()


def test_LilyPondGrobNameManager___setattr___18():
    """
    Override LilyPond abjad.NoteColumn grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).note_column.ignore_collision = True

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override NoteColumn.ignore-collision = ##t
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )

    assert abjad.inspect(staff).is_wellformed()


def test_LilyPondGrobNameManager___setattr___19():
    """
    Override LilyPond abjad.NoteHead grob.
    """

    note = abjad.Note(1, (1, 4))
    abjad.override(note).note_head.style = 'cross'

    assert abjad.override(note).note_head.style == 'cross'
    assert format(note) == abjad.String.normalize(
        r"""
        \once \override NoteHead.style = #'cross
        cs'4
        """
        )

    del(abjad.override(note).note_head.style)
    assert format(note.note_head) == "cs'"


def test_LilyPondGrobNameManager___setattr___20():
    """
    Notehead styles are handled just like all other grob abjad.overrides.
    """

    note = abjad.Note(1, (1, 4))
    abjad.override(note).note_head.style = 'mystrangehead'

    assert abjad.override(note).note_head.style == 'mystrangehead'
    assert format(note) == abjad.String.normalize(
        r"""
        \once \override NoteHead.style = #'mystrangehead
        cs'4
        """
        )

    del(abjad.override(note).note_head.style)
    assert format(note.note_head) == "cs'"


def test_LilyPondGrobNameManager___setattr___21():
    """
    Notehead style abjad.overrides are handled just like all other
    note_head grob abjad.overrides, even for note_heads in chords.
    """

    chord = abjad.Chord([1, 2, 3], (1, 4))
    chord.note_heads[0].tweaks.style = 'harmonic'

    assert format(chord) == abjad.String.normalize(
        r"""
        <
            \tweak style #'harmonic
            cs'
            d'
            ef'
        >4
        """
        )


def test_LilyPondGrobNameManager___setattr___22():
    """
    Notehead shape style abjad.overrides are just normal grob abjad.overrides.
    """

    note = abjad.Note(1, (1, 4))
    abjad.override(note).note_head.style = 'triangle'

    assert abjad.override(note).note_head.style == 'triangle'
    assert format(note) == abjad.String.normalize(
        r"""
        \once \override NoteHead.style = #'triangle
        cs'4
        """
        )

    del(abjad.override(note).note_head.style)
    assert format(note) == "cs'4"


def test_LilyPondGrobNameManager___setattr___23():
    """
    Notehead solfege style abjad.overrides are just normal grob abjad.overrides.
    Modern versions of LilyPond now handles solfege abjad.overrides
    correctly.
    """

    note = abjad.Note(1, (1, 4))
    abjad.override(note).note_head.style = 'do'

    assert abjad.override(note).note_head.style == 'do'
    assert format(note) == abjad.String.normalize(
        r"""
        \once \override NoteHead.style = #'do
        cs'4
        """
        )

    del(abjad.override(note).note_head.style)
    assert format(note) == "cs'4"


def test_LilyPondGrobNameManager___setattr___24():
    """
    Override LilyPond abjad.NoteHead grob.
    """

    note = abjad.Note(13, (1, 4))
    abjad.override(note).note_head.transparent = True

    assert abjad.override(note).note_head.transparent
    assert format(note) == abjad.String.normalize(
        r"""
        \once \override NoteHead.transparent = ##t
        cs''4
        """
        )

    del(abjad.override(note).note_head.transparent)
    assert format(note) == "cs''4"


def test_LilyPondGrobNameManager___setattr___25():
    """
    Override LilyPond abjad.NoteHead grob.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    abjad.override(voice).note_head.color = 'red'

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        \with
        {
            \override NoteHead.color = #red
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )

    assert abjad.inspect(voice).is_wellformed()


def test_LilyPondGrobNameManager___setattr___26():
    """
    Override LilyPond RehearsalMark grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).rehearsal_mark.staff_padding = 2
    abjad.override(staff).rehearsal_mark.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override RehearsalMark.Y-extent = #'(-1.5 . 1.5)
            \override RehearsalMark.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___27():
    """
    Override LilyPond abjad.Rest grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).rest.transparent = True

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override Rest.transparent = ##t
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___28():
    """
    Override LilyPond Script grob.
    """

    note = abjad.Note("c'4")
    articulation = abjad.Articulation('staccato')
    abjad.attach(articulation, note)
    abjad.override(note).script.color = 'red'

    assert format(note) == abjad.String.normalize(
        r"""
        \once \override Script.color = #red
        c'4
        - \staccato
        """
        )


def test_LilyPondGrobNameManager___setattr___29():
    """
    Override LilyPond Script grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).script.staff_padding = 2
    abjad.override(staff).script.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override Script.Y-extent = #'(-1.5 . 1.5)
            \override Script.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___30():
    """
    Override LilyPond SpacingSpanner grob.
    """

    score = abjad.Score([])
    abjad.override(score).spacing_spanner.strict_grace_spacing = True
    abjad.override(score).spacing_spanner.strict_note_spacing = True
    abjad.override(score).spacing_spanner.uniform_stretching = True

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            \override SpacingSpanner.strict-grace-spacing = ##t
            \override SpacingSpanner.strict-note-spacing = ##t
            \override SpacingSpanner.uniform-stretching = ##t
        }
        <<
        >>
        """
        )

    assert not len(score)


def test_LilyPondGrobNameManager___setattr___31():
    """
    Override LilyPond SpanBar grob.
    """

    score, treble, bass = abjad.Score.make_piano_score()
    notes = [abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("e'8"), abjad.Note("f'8")]
    treble.extend(notes)
    notes = [abjad.Note("c'8"), abjad.Note("d'8"), abjad.Note("e'8"), abjad.Note("f'8")]
    bass.extend(notes)
    abjad.override(score).span_bar.color = 'red'
    abjad.attach(abjad.Clef('treble'), treble[0])
    abjad.attach(abjad.Clef('bass'), bass[0])

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            \override SpanBar.color = #red
        }
        <<
            \new PianoStaff
            <<
                \context Staff = "Treble Staff"
                {
                    \clef "treble"
                    c'8
                    d'8
                    e'8
                    f'8
                }
                \context Staff = "Bass Staff"
                {
                    \clef "bass"
                    c'8
                    d'8
                    e'8
                    f'8
                }
            >>
        >>
        """
        )

    assert abjad.inspect(score).is_wellformed()


def test_LilyPondGrobNameManager___setattr___32():
    """
    Override LilyPond StaffSymbol grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).staff_symbol.color = 'red'

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override StaffSymbol.color = #red
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___33():
    """
    Override LilyPond StaffSymbol grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff[2]).staff.staff_symbol.color = 'red'

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            c'8
            d'8
            \once \override Staff.StaffSymbol.color = #red
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___34():
    """
    Override LilyPond StaffSymbol grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).staff_symbol.line_positions = \
        abjad.SchemeVector([-4, -2, 2, 4])

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override StaffSymbol.line-positions = #'(-4 -2 2 4)
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___35():
    """
    Override LilyPond Stem grob.
    """

    note = abjad.Note(0, (1, 16))
    abjad.override(note).stem.stroke_style = \
        abjad.Scheme('grace', force_quotes=True)

    assert format(note) == abjad.String.normalize(
        r"""
        \once \override Stem.stroke-style = #"grace"
        c'16
        """
        )


def test_LilyPondGrobNameManager___setattr___36():
    """
    Override LilyPond StemTremolo grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).stem_tremolo.slope = 0.5
    abjad.override(staff).stem_tremolo.staff_padding = 2

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override StemTremolo.slope = #0.5
            \override StemTremolo.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___37():
    """
    Override LilyPond SystemStartBar grob.
    """

    score = abjad.Score([abjad.StaffGroup([abjad.Staff("c'8 c'8 c'8 c'8 c'8 c'8 c'8 c'8")])])
    abjad.override(score).system_start_bar.collapse_height = 0
    abjad.override(score).system_start_bar.color = 'red'

    assert format(score) == abjad.String.normalize(
        r"""
        \new Score
        \with
        {
            \override SystemStartBar.collapse-height = #0
            \override SystemStartBar.color = #red
        }
        <<
            \new StaffGroup
            <<
                \new Staff
                {
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                    c'8
                }
            >>
        >>
        """
        )


def test_LilyPondGrobNameManager___setattr___38():
    """
    Override LilyPond Tie grob.
    """

    note = abjad.Note("c'4")
    abjad.override(note).tie.color = 'red'

    assert format(note) == abjad.String.normalize(
        r"""
        \once \override Tie.color = #red
        c'4
        """
        )


def test_LilyPondGrobNameManager___setattr___39():
    """
    Override LilyPond abjad.TimeSignature grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).time_signature.transparent = True

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override TimeSignature.transparent = ##t
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___40():
    """
    Override LilyPond abjad.TimeSignature grob.
    """

    measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
    abjad.override(measure).time_signature.transparent = True

    assert format(measure) == abjad.String.normalize(
        r"""
        {   % measure
            \override TimeSignature.transparent = ##t
            \time 4/8
            c'8
            d'8
            e'8
            f'8
            \revert TimeSignature.transparent
        }   % measure
        """
        )


def test_LilyPondGrobNameManager___setattr___41():
    """
    Override LilyPond abjad.TimeSignature grob.
    """

    measure = abjad.Measure((4, 8), "c'8 d'8 e'8 f'8")
    abjad.override(measure).staff.time_signature.transparent = True

    assert format(measure) == abjad.String.normalize(
        r"""
        {   % measure
            \override Staff.TimeSignature.transparent = ##t
            \time 4/8
            c'8
            d'8
            e'8
            f'8
            \revert Staff.TimeSignature.transparent
        }   % measure
        """
        )


def test_LilyPondGrobNameManager___setattr___42():
    """
    Override LilyPond TrillPitchAccidental grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).trill_pitch_accidental.staff_padding = 2
    abjad.override(staff).trill_pitch_accidental.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override TrillPitchAccidental.Y-extent = #'(-1.5 . 1.5)
            \override TrillPitchAccidental.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___43():
    """
    Override LilyPond abjad.TupletBracket grob.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    abjad.override(voice).tuplet_bracket.direction = abjad.Down

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        \with
        {
            \override TupletBracket.direction = #down
        }
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
        )

    assert abjad.inspect(voice).is_wellformed()


def test_LilyPondGrobNameManager___setattr___44():
    """
    Override LilyPond abjad.TupletBracket grob.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    abjad.override(voice[1]).tuplet_bracket.direction = abjad.Down

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \once \override TupletBracket.direction = #down
            d'8
            e'8
            f'8
            ]
        }
        """
        )

    assert abjad.inspect(voice).is_wellformed()


def test_LilyPondGrobNameManager___setattr___45():
    """
    Override LilyPond abjad.TupletNumber grob.
    """

    tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
    abjad.override(tuplet).tuplet_number.fraction = True

    assert format(tuplet) == abjad.String.normalize(
        r"""
        \override TupletNumber.fraction = ##t
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        \revert TupletNumber.fraction
        """
        )

    assert abjad.inspect(tuplet).is_wellformed()


def test_LilyPondGrobNameManager___setattr___46():
    """
    Override LilyPond abjad.TupletNumber grob.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    abjad.override(voice).tuplet_number.fraction = True

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        \with
        {
            \override TupletNumber.fraction = ##t
        }
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
        )

    assert abjad.inspect(voice).is_wellformed()


def test_LilyPondGrobNameManager___setattr___47():
    """
    Override LilyPond abjad.TupletNumber grob.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    abjad.override(voice[1]).tuplet_number.fraction = True

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        {
            c'8
            [
            \once \override TupletNumber.fraction = ##t
            d'8
            e'8
            f'8
            ]
        }
        """
        )

    assert abjad.inspect(voice).is_wellformed()


def test_LilyPondGrobNameManager___setattr___48():
    """
    Override LilyPond abjad.TupletNumber grob.
    """

    voice = abjad.Voice("c'8 d'8 e'8 f'8")
    beam = abjad.Beam()
    abjad.attach(beam, voice[:])
    abjad.override(voice).tuplet_number.text = abjad.Markup('6:4')

    assert format(voice) == abjad.String.normalize(
        r"""
        \new Voice
        \with
        {
            \override TupletNumber.text = \markup { 6:4 }
        }
        {
            c'8
            [
            d'8
            e'8
            f'8
            ]
        }
        """
        )

    assert abjad.inspect(voice).is_wellformed()


def test_LilyPondGrobNameManager___setattr___49():
    """
    Override LilyPond VerticalAlignment grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).vertical_alignment.staff_padding = 2
    abjad.override(staff).vertical_alignment.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override VerticalAlignment.Y-extent = #'(-1.5 . 1.5)
            \override VerticalAlignment.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___50():
    """
    Override LilyPond VerticalAxis grob.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    abjad.override(staff).vertical_axis_group.staff_padding = 2
    abjad.override(staff).vertical_axis_group.Y_extent = (-1.5, 1.5)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        \with
        {
            \override VerticalAxisGroup.Y-extent = #'(-1.5 . 1.5)
            \override VerticalAxisGroup.staff-padding = #2
        }
        {
            c'8
            d'8
            e'8
            f'8
        }
        """
        )


def test_LilyPondGrobNameManager___setattr___51():
    """
    InputSetExpression attribute on erroneous grob name raises exception.
    """

    note = abjad.Note("c'8")
    assert pytest.raises(Exception, 'override(note).foo = True')
