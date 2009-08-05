from abjad import *
import py.test


def test_pianopedal_spanner_01( ):
   t = Staff(construct.run(4))
   p = PianoPedal(t[:])

   r'''\new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
   }'''

   assert check.wf(t)
   assert p.kind == 'sustain'
   assert p.style == 'mixed'
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\sustainOn\n\tc'8\n\tc'8\n\tc'8 \\sustainOff\n}"


def test_pianopedal_spanner_02( ):
   '''PianoPedal spanner supports sostenuto pedal.'''

   t = Staff(construct.run(4))
   p = PianoPedal(t[:])
   p.kind = 'sostenuto'

   r'''\new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \sostenutoOn
        c'8
        c'8
        c'8 \sostenutoOff
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\sostenutoOn\n\tc'8\n\tc'8\n\tc'8 \\sostenutoOff\n}"


def test_pianopedal_spanner_03( ):
   '''PianoPedal spanner supports una corda pedal.'''

   t = Staff(construct.run(4))
   p = PianoPedal(t[:])
   p.kind = 'corda'

   r'''\new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \unaCorda
        c'8
        c'8
        c'8 \treCorde
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\unaCorda\n\tc'8\n\tc'8\n\tc'8 \\treCorde\n}"


def test_pianopedal_spanner_04( ):
   '''PianoPedal spanner supports text style.'''

   t = Staff(construct.run(4))
   p = PianoPedal(t[:])
   assert p.kind == 'sustain'
   p.style = 'text'

   r'''\new Staff {
        \set Staff.pedalSustainStyle = #'text
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'text\n\tc'8 \\sustainOn\n\tc'8\n\tc'8\n\tc'8 \\sustainOff\n}"


def test_pianopedal_spanner_05( ):
   '''PianoPedal spanner supports bracket style.'''

   t = Staff(construct.run(4))
   p = PianoPedal(t[:])
   assert p.kind == 'sustain'
   p.style = 'bracket'

   r'''\new Staff {
        \set Staff.pedalSustainStyle = #'bracket
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'bracket\n\tc'8 \\sustainOn\n\tc'8\n\tc'8\n\tc'8 \\sustainOff\n}"


def test_pianopedal_spanner_06( ):
   '''Consecutive dovetailing PianoPedal spanners format correctly.'''

   t = Staff(construct.run(8))
   PianoPedal(t[:4])
   PianoPedal(t[3:])

   r'''\new Staff {
      \set Staff.pedalSustainStyle = #'mixed
      c'8 \sustainOn
      c'8
      c'8
      \set Staff.pedalSustainStyle = #'mixed
      c'8 \sustainOff \sustainOn
      c'8
      c'8
      c'8
      c'8 \sustainOff
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\sustainOn\n\tc'8\n\tc'8\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\sustainOff \\sustainOn\n\tc'8\n\tc'8\n\tc'8\n\tc'8 \\sustainOff\n}"


def test_pianopedal_spanner_07( ):
   '''The 'kind' and 'style' attributes raise ValueError as needed.'''

   t = Staff(construct.run(4))
   p = PianoPedal(t)

   assert py.test.raises(ValueError, 'p.kind = "abc"')
   assert py.test.raises(ValueError, 'p.style = "abc"')
