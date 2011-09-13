from abjad import *


def test_leaftools_color_leaves_in_expr_01():

    t = Staff([Note(1, (3, 16)), Rest((3, 16)), skiptools.Skip((3, 16)),
      Chord([0, 1, 9], (3, 16))])
    leaftools.color_leaves_in_expr(t, 'red')

    r'''
    \new Staff {
      \once \override Accidental #'color = #red
      \once \override Dots #'color = #red
      \once \override NoteHead #'color = #red
      cs'8.
      \once \override Dots #'color = #red
      \once \override Rest #'color = #red
      r8.
      s8.
      \once \override Accidental #'color = #red
      \once \override Dots #'color = #red
      \once \override NoteHead #'color = #red
      <c' cs' a'>8.
    }
    '''

    assert t.format == "\\new Staff {\n\t\\once \\override Accidental #'color = #red\n\t\\once \\override Dots #'color = #red\n\t\\once \\override NoteHead #'color = #red\n\tcs'8.\n\t\\once \\override Dots #'color = #red\n\t\\once \\override Rest #'color = #red\n\tr8.\n\ts8.\n\t\\once \\override Accidental #'color = #red\n\t\\once \\override Dots #'color = #red\n\t\\once \\override NoteHead #'color = #red\n\t<c' cs' a'>8.\n}"
