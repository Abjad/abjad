from abjad import *
import py.test


def test_pianopedal_spanner_01( ):
   t = Staff(run(4))
   p = PianoPedal(t[:])
   assert p.type == 'sustain'
   assert p.style == 'mixed'
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\sustainOn\n\tc'8\n\tc'8\n\tc'8 \\sustainOff\n}"
   r'''
   \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
   }
   '''


def test_pianopedal_spanner_02( ):
   '''PianoPedal spanner supports sostenuto pedal.'''
   t = Staff(run(4))
   p = PianoPedal(t[:])
   p.type = 'sostenuto'
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\sostenutoOn\n\tc'8\n\tc'8\n\tc'8 \\sostenutoOff\n}"
   r'''
   \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \sostenutoOn
        c'8
        c'8
        c'8 \sostenutoOff
   }
   '''


def test_pianopedal_spanner_03( ):
   '''PianoPedal spanner supports una corda pedal.'''
   t = Staff(run(4))
   p = PianoPedal(t[:])
   p.type = 'corda'
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\unaCorda\n\tc'8\n\tc'8\n\tc'8 \\treCorde\n}"
   r'''
   \new Staff {
        \set Staff.pedalSustainStyle = #'mixed
        c'8 \unaCorda
        c'8
        c'8
        c'8 \treCorde
   }
   '''


def test_pianopedal_spanner_04( ):
   '''PianoPedal spanner supports text style.'''
   t = Staff(run(4))
   p = PianoPedal(t[:])
   assert p.type == 'sustain'
   p.style = 'text'
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'text\n\tc'8 \\sustainOn\n\tc'8\n\tc'8\n\tc'8 \\sustainOff\n}"
   r'''
   \new Staff {
        \set Staff.pedalSustainStyle = #'text
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
   }
   '''


def test_pianopedal_spanner_05( ):
   '''PianoPedal spanner supports bracket style.'''
   t = Staff(run(4))
   p = PianoPedal(t[:])
   assert p.type == 'sustain'
   p.style = 'bracket'
   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'bracket\n\tc'8 \\sustainOn\n\tc'8\n\tc'8\n\tc'8 \\sustainOff\n}"
   r'''
   \new Staff {
        \set Staff.pedalSustainStyle = #'bracket
        c'8 \sustainOn
        c'8
        c'8
        c'8 \sustainOff
   }
   '''


## TODO: Make this sixth test work by fixing the order in which
##       start- and stop-indications for spanners print at format-time.

#def test_pianopedal_spanner_06( ):
#   '''Consecutive dovetailing PianoPedal spanners format correctly.'''
#   t = Staff(run(8))
#   PianoPedal(t[:4])
#   PianoPedal(t[3:])
#   assert t.format == "\\new Staff {\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\sustainOn\n\tc'8\n\tc'8\n\t\\set Staff.pedalSustainStyle = #'mixed\n\tc'8 \\sustainOn \\sustainOff\n\tc'8\n\tc'8\n\tc'8\n\tc'8 \\sustainOff\n}"
#   r'''
#   \new Staff {
#        \set Staff.pedalSustainStyle = #'mixed
#        c'8 \sustainOn
#        c'8
#        c'8
#        \set Staff.pedalSustainStyle = #'mixed
#        c'8 \sustainOn \sustainOff
#        c'8
#        c'8
#        c'8
#        c'8 \sustainOff
#   }
#   '''


### VALUE ERRORS ###

def test_pianopedal_spanner_07( ):
   '''Styles and types not knows raise ValueError.'''
   t = Staff(run(4))
   p = PianoPedal(t)
   assert py.test.raises(ValueError, 'p.type = "abc"')
   assert py.test.raises(ValueError, 'p.style = "abc"')
