import abjad
from abjad import rmakers


def test_DurationSpecifier_01():
    """
    DurationSpecifier does not leave parent references.
    """

    beam_specifier = rmakers.BeamSpecifier(
        beam_each_division=True,
        beam_divisions_together=False,
        use_feather_beams=False,
        )

    duration_specifier = rmakers.DurationSpecifier(
        decrease_monotonic=True,
        forbid_meter_rewriting=False,
        rewrite_meter=True,
        spell_metrically='unassignable',
        )

    logical_tie_masks = [abjad.silence([0], 2)]

    talea = rmakers.Talea(counts=[1, 2, 3, 4], denominator=16)

    maker = rmakers.TaleaRhythmMaker(
        beam_specifier=beam_specifier,
        duration_specifier=duration_specifier,
        logical_tie_masks=logical_tie_masks,
        talea=talea,
        )

    divisions = [abjad.TimeSignature((3, 8)), abjad.TimeSignature((2, 4)), abjad.TimeSignature((5, 16))]

    result = maker(divisions)

    staff = abjad.Staff(result)

    assert format(staff) == abjad.String.normalize(
        r"""
        \new Staff
        {
            r16
            c'16
            ~
            [
            c'16
            ]
            r8.
            c'4
            r16
            c'16
            ~
            [
            c'16
            ]
            r16
            r8
            c'8.
        }
        """)
