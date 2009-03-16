from abjad.component.component import _Component
from abjad import *


def test_parentage_containment_signature_str_01( ):
   '''Containment signature of leaf 2.
      Signature contains no explicit voice, staff or score.
      Outermost sequentials acts as signature root.'''

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

   '''abjad> print t.leaves[2].parentage._containmentSignature

       root: Sequential-4274576 (4274576)
      score: 
      staff: 
      voice: 
       self: Note-5358192'''


def test_parentage_containment_signature_str_02( ):
   '''Containment signature of leaf 2.
      Signature contains named voice 'foo'.
      Signature contains neither staff nor score.
      Named voice 'foo' acts as signature root.'''

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

   '''abjad> print t.leaves[2].parentage._containmentSignature

       root: Voice-foo (4274608)
      score: 
      staff: 
      voice: Voice-foo
       self: Note-5358256'''


def test_parentage_containment_signature_str_03( ):
   '''Containment signature of leaf 2.
      Signature contains anonymous voice.
      Signature contains neither staff nor score.
      Anonymous voice acts as signature root.'''

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

   '''abjad> print t.leaves[2].parentage._containmentSignature

       root: Voice-4274576 (4274576)
      score: 
      staff: 
      voice: Voice-4274576
       self: Note-5358224'''


def test_parentage_containment_signature_str_04( ):
   '''Containment signature for leaf 2.
      Signature contains innermost anonymous voice.
      Signature contains neither staff nor score.
      Outermost anonymous voice acts as signature root.'''

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

   '''abjad> print t.leaves[2].parentage._containmentSignature

       root: Voice-4274576 (4274576)
      score: 
      staff: 
      voice: Voice-5357872
       self: Note-5358320'''

      
def test_parentage_containment_signature_str_05( ):
   '''Containment signature for leaf 2.
      Signature contains named voice 'foo'.
      Signature contains neither staff nor score.
      Outermost instance of named voice 'foo' acts as signature root.'''

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

   '''abjad> print t.leaves[0].parentage._containmentSignature

       root: Voice-foo (4274640)
      score: 
      staff: 
      voice: Voice-foo
       self: Note-5362480'''


def test_parentage_containment_signature_str_06( ):
   '''Containment signature of leaf 2.
      Signature contains named 'voicefoo' and 'staff1'.
      Signature contains no score.
      Outermost sequential acts as signature root.'''

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

   '''abjad> print t.leaves[2].parentage._containmentSignature

       root: Sequential-4393200 (4393200)
      score: 
      staff: Staff-staff2
      voice: Voice-voicefoo
       self: Note-5334832'''

   
def test_parentage_containment_signature_str_07( ):

   t = Sequential(run(2))
   t[1:1] = Parallel(Voice(run(1)) * 2) * 2
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
         }
         \context Voice = "soprano" {
            \override NoteHead #'color = #red
            e'8
         }
      >>
      <<
         \context Voice = "alto" {
            f'8
         }
         \context Voice = "soprano" {
            g'8
            \revert NoteHead #'color
         }
      >>
      a'8
   }'''
   
   '''abjad> print t.leaves[2].parentage._containmentSignature

       root: Sequential-4274704 (4274704)
      score: 
      staff: 
      voice: Voice-soprano
       self: Note-4370288'''


def test_parentage_containment_signature_str_08( ):
   '''Unicorporated leaves carry different containment signatures.'''

   t = Note(0, (1, 8))
  
   '''abjad> print t.parentage._containmentSignature

       root: Note-5494544 (5494544)
      score: 
      staff: 
      voice: 
       self: Note-5494544'''


def test_parentage_containment_signature_str_09( ):

   t = Staff([Voice([Note(0, (1, 8))])])
   t.invocation.name = 'staff'
   t[0].invocation.name = 'voice'

   '''abjad> print t.leaves[0].parentage._containmentSignature

    root: Staff-staff (4297200)
   score: 
   staff: Staff-staff
   voice: Voice-voice
    self: Note-4247440'''
