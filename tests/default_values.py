import abjad

class_to_default_values = {
    abjad.io.AbjadGrapher: (abjad.Note("c'4"),),
    abjad.io.Illustrator: (abjad.Note("c'4"),),
    abjad.io.LilyPondIO: (abjad.Note("c'4"),),
    abjad.io.Player: (abjad.Note("c'4"),),
    abjad.parsers.parser.MarkupCommand: (r"\hcenter-in",),
    abjad.Articulation: ("staccato",),
    abjad.ColorFingering: (0,),
    abjad.Line: ("text",),
    abjad.Markup: (r"\markup Allegro",),
    abjad.MetricModulation: (abjad.Note("c'4"), abjad.Note("c'4.")),
    abjad.MetronomeMark: ((1, 4), 90),
    abjad.PitchInequality: ("&", "C4"),
    abjad.StringNumber: ([1],),
    abjad.TimeSignature: ((4, 4),),
    abjad.Tuning: ("g d' a' e''",),
}
