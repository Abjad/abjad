from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals


def test_intervaltreetools_make_polyphonic_percussion_score_from_nonoverlapping_trees_01():
    a = BoundedInterval(0, 3, {})
    b = BoundedInterval(6, 12, {})
    c = BoundedInterval(9, 15, {})
    tree = IntervalTree([a, b, c])
    trees = explode_intervals_compactly(tree)
    lily = make_polyphonic_percussion_score_from_nonoverlapping_trees(trees)
    assert lily.score_block[0].format == '\\new Score \\with {\n\t\\override Glissando #\'bound-details = #\'((right (attach-dir . 0) (padding . 0.5)) (left (attach-dir . 0) (padding . 0.5)))\n\t\\override Glissando #\'breakable = ##t\n\t\\override Glissando #\'thickness = #5\n\t\\override NoteHead #\'style = #\'harmonic\n\t\\override Rest #\'transparent = ##t\n\t\\override SpacingSpanner #\'strict-note-spacing = ##t\n\t\\override SpacingSpanner #\'uniform-stretching = ##t\n\tproportionalNotationDuration = #(ly:make-moment 1 32)\n} <<\n\t\\new Staff \\with {\n\t\t\\override StaffSymbol #\'line-count = #2\n\t} <<\n\t\t\\clef "percussion"\n\t\t\\new Voice \\with {\n\t\t\t\\remove Forbid_line_break_engraver\n\t\t} {\n\t\t\tb1 * 3 \\glissando\n\t\t\t\\once \\override NoteHead #\'transparent = ##t\n\t\t\tb1 * 3\n\t\t\tb1 * 6 \\glissando\n\t\t\t\\once \\override NoteHead #\'transparent = ##t\n\t\t\tb1\n\t\t}\n\t\t\\new Voice \\with {\n\t\t\t\\remove Forbid_line_break_engraver\n\t\t} {\n\t\t\tr1 * 9\n\t\t\td\'1 * 6 \\glissando\n\t\t\t\\once \\override NoteHead #\'transparent = ##t\n\t\t\td\'1\n\t\t}\n\t>>\n>>'
