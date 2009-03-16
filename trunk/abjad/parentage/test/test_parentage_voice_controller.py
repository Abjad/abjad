from abjad import *


def test_parentage_voice_controller_01( ):
   '''Return reference to first context in parentage of client,
      otherwise None.'''

   t = Sequential(run(4))
   t.insert(2, Parallel(Sequential(run(2)) * 2))
   diatonicize(t)
   t.notehead.color = 'red'

   r'''{
           \override NoteHead #'color = #red
           c'8
           d'8
           <<
                   {
                           e'8
                           f'8
                   }
                   {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
           \revert NoteHead #'color
   }'''

   leaves = t.leaves
   
   assert leaves[0].parentage._voiceController is None
   assert leaves[1].parentage._voiceController is None
   assert leaves[2].parentage._voiceController is None
   assert leaves[3].parentage._voiceController is None
   assert leaves[4].parentage._voiceController is None
   assert leaves[5].parentage._voiceController is None
   assert leaves[6].parentage._voiceController is None
   assert leaves[7].parentage._voiceController is None


def test_parentage_voice_controller_02( ):
   '''Return reference to first context in parentage of client,
      otherwise None.'''

   t = Voice(run(4))
   t.invocation.name = 'foo'
   t.insert(2, Parallel(Sequential(run(2)) * 2))
   diatonicize(t)
   t.notehead.color = 'red'

   r'''\context Voice = "foo" \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   {
                           e'8
                           f'8
                   }
                   {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }'''

   parallel = t[2]
   leaves = t.leaves

   assert leaves[0].parentage._voiceController is t
   assert leaves[1].parentage._voiceController is t
   assert leaves[2].parentage._voiceController is t
   assert leaves[3].parentage._voiceController is t
   assert leaves[4].parentage._voiceController is t
   assert leaves[5].parentage._voiceController is t
   assert leaves[6].parentage._voiceController is t
   assert leaves[7].parentage._voiceController is t


def test_parentage_voice_controller_03( ):

   t = Voice(run(4))
   t.insert(2, Parallel(Sequential(run(2)) * 2))
   diatonicize(t)
   t.notehead.color = 'red'

   r'''\new Voice \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   {
                           e'8
                           f'8
                   }
                   {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }'''

   for leaf in t.leaves:
      assert leaf.parentage._voiceController is t


def test_parentage_voice_controller_04( ):

   t = Voice(run(4))
   t.insert(2, Parallel(Voice(run(2)) * 2))
   diatonicize(t)
   t.notehead.color = 'red'

   r'''\new Voice \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   \new Voice {
                           e'8
                           f'8
                   }
                   \new Voice {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }'''

   anonymous1 = t[2][0]
   anonymous2 = t[2][1]
   leaves = t.leaves

   assert leaves[0].parentage._voiceController is t
   assert leaves[1].parentage._voiceController is t
   assert leaves[2].parentage._voiceController is anonymous1
   assert leaves[3].parentage._voiceController is anonymous1
   assert leaves[4].parentage._voiceController is anonymous2
   assert leaves[5].parentage._voiceController is anonymous2
   assert leaves[6].parentage._voiceController is t
   assert leaves[7].parentage._voiceController is t


def test_parentage_voice_controller_05( ):

   t = Voice(run(4))
   t.invocation.name = 'foo'
   t.insert(2, Parallel(Voice(run(2)) * 2))
   t[2][0].invocation.name = 'foo'
   diatonicize(t)
   t.notehead.color = 'red'

   r'''\context Voice = "foo" \with {
           \override NoteHead #'color = #red
   } {
           c'8
           d'8
           <<
                   \context Voice = "foo" {
                           e'8
                           f'8
                   }
                   \new Voice {
                           g'8
                           a'8
                   }
           >>
           b'8
           c''8
   }
   '''

   foo_outer = t
   foo_inner = t[2][0]
   anonymous = t[2][1] 
   leaves = t.leaves

   assert leaves[0].parentage._voiceController is foo_outer
   assert leaves[1].parentage._voiceController is foo_outer
   assert leaves[2].parentage._voiceController is foo_inner
   assert leaves[3].parentage._voiceController is foo_inner
   assert leaves[4].parentage._voiceController is anonymous
   assert leaves[5].parentage._voiceController is anonymous
   assert leaves[6].parentage._voiceController is foo_outer
   assert leaves[7].parentage._voiceController is foo_outer


def test_parentage_voice_controller_06( ):

   t = Sequential(Staff([Voice(scale(2))]) * 2)
   t[0].invocation.name = 'staff1'
   t[1].invocation.name = 'staff2'
   t[0][0].invocation.name = 'voicefoo'
   t[1][0].invocation.name = 'voicefoo'
   diatonicize(t)
   Beam(t.leaves)

   r'''{
           \context Staff = "staff1" {
                   \context Voice = "voicefoo" {
                           c'8 [
                           d'8
                   }
           }
           \context Staff = "staff2" {
                   \context Voice = "voicefoo" {
                           e'8
                           f'8 ]
                   }
           }
   }'''

   voicefoo_staff1 = t[0][0]
   voicefoo_staff2 = t[1][0]
   leaves = t.leaves

   assert leaves[0].parentage._voiceController is voicefoo_staff1
   assert leaves[1].parentage._voiceController is voicefoo_staff1
   assert leaves[2].parentage._voiceController is voicefoo_staff2
   assert leaves[3].parentage._voiceController is voicefoo_staff2

   
def test_parentage_voice_controller_07( ):

   t = Sequential(run(2))
   t[1:1] = Parallel(Voice(run(2)) * 2) * 2
   t[1][0].invocation.name = 'alto'
   t[1][1].invocation.name = 'soprano'
   t[2][0].invocation.name = 'alto'
   t[2][1].invocation.name = 'soprano'
   diatonicize(t)

   t[1][1][0].formatter.before.append(r"\override NoteHead #'color = #red")
   t[2][1][-1].formatter.after.append(r"\revert NoteHead #'color")

   r'''{
           c'8
           <<
                   \context Voice = "alto" {
                           d'8
                           e'8
                   }
                   \context Voice = "soprano" {
                           \override NoteHead #'color = #red
                           f'8
                           g'8
                   }
           >>
           <<
                   \context Voice = "alto" {
                           a'8
                           b'8
                   }
                   \context Voice = "soprano" {
                           c''8
                           d''8
                           \revert NoteHead #'color
                   }
           >>
           e''8
   }'''

   alto_first = t[1][0]
   soprano_first = t[1][1]
   alto_second = t[2][0]
   soprano_second = t[2][1]
   leaves = t.leaves

   assert leaves[0].parentage._voiceController is None
   assert leaves[1].parentage._voiceController is alto_first
   assert leaves[2].parentage._voiceController is alto_first
   assert leaves[3].parentage._voiceController is soprano_first
   assert leaves[4].parentage._voiceController is soprano_first
   assert leaves[5].parentage._voiceController is alto_second
   assert leaves[6].parentage._voiceController is alto_second
   assert leaves[7].parentage._voiceController is soprano_second
   assert leaves[8].parentage._voiceController is soprano_second
   assert leaves[9].parentage._voiceController is None
