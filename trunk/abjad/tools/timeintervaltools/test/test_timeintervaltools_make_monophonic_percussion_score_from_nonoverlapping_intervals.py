from fractions import Fraction
from abjad.tools.timeintervaltools import *


def test_timeintervaltools_make_monophonic_percussion_score_from_nonoverlapping_intervals_01():
    a = TimeInterval(0, Fraction(3, 4), {})
    b = TimeInterval(Fraction(5, 4), Fraction(7, 4), {})
    tree = TimeIntervalTree([a, b])
    score = make_monophonic_percussion_score_from_nonoverlapping_intervals(tree)
    assert score.lilypond_format == '\\new Score \\with {\n\t\\override Glissando #\'bound-details = #\'((right (attach-dir . 0) (padding . 0.5)) (left (attach-dir . 0) (padding . 0.5)))\n\t\\override Glissando #\'breakable = ##t\n\t\\override Glissando #\'thickness = #5\n\t\\override NoteHead #\'style = #\'harmonic\n\t\\override Rest #\'transparent = ##t\n\t\\override SpacingSpanner #\'strict-note-spacing = ##t\n} <<\n\t\\new Staff \\with {\n\t\t\\override StaffSymbol #\'line-count = #1\n\t} {\n\t\t\\clef "percussion"\n\t\tc\'1 * 3/4 \\glissando\n\t\t\\once \\override NoteHead #\'transparent = ##t\n\t\tc\'1 * 1/2\n\t\tc\'1 * 1/2 \\glissando\n\t\t\\once \\override NoteHead #\'transparent = ##t\n\t\tc\'1\n\t}\n>>'
