from abjad import *


### TODO - remove this test file in favor of die( ) test file ###

def test_del_beam_spanner_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[0])
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert check(t)
   #del(t[0].spanners[0])
   t[0].spanners.mine( )[0].die( )
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert check(t)
   Beam(t[0])
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert check(t)
   #del(t.spanners[0])
   #assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   #assert check(t)
   

def test_del_beam_spanner_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert check(t)
   #del(t[0].spanners[0])
   t[0].spanners.mine( )[0].die( )
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert check(t)
   Beam(t[ : 4])
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert check(t)
   #del(t.spanners[0])
   #assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   #assert check(t)
