from abjad import *


def test_del_beam_spanner_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[0])
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert t.tester.testAll(ret = True)
   del(t[0].spanners[0])
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert t.tester.testAll(ret = True)
   Beam(t[0])
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert t.tester.testAll(ret = True)
   del(t.spanners[0])
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert t.tester.testAll(ret = True)
   

def test_del_beam_spanner_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert t.tester.testAll(ret = True)
   del(t[0].spanners[0])
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert t.tester.testAll(ret = True)
   Beam(t[ : 4])
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert t.tester.testAll(ret = True)
   del(t.spanners[0])
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   assert t.tester.testAll(ret = True)
