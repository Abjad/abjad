from abjad import *


def test_container_setitem_01( ):
   '''
   Containers set single leaves correctly in an unspanned structure.
   '''

   t = Staff(scale(4))
   t[2:2] = [Note(7, (1, 8))]

   r'''
   \new Staff {
           c'8
           d'8
           g'8
           e'8
           f'8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\tg'8\n\te'8\n\tf'8\n}"
   assert check(t)


def test_container_setitem_02( ):
   '''
   Containers set single leaves correctly in a spanned structure.
   You must spanned newly set leaves by hand, if desired.
   '''

   t = Staff(scale(4))
   p = Beam(t[ : ])
   note = Note(7, (1, 8))
   t[2:2] = [note]
   p[2:2] = [note]

   r'''
   \new Staff {
           c'8 [
           d'8
           g'8
           e'8
           f'8 ]
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\tg'8\n\te'8\n\tf'8 ]\n}"
   assert check(t)
   

def test_container_setitem_03( ):
   '''
   Containers set sequences of notes correctly.
   Spanners set sequences of notes correctly.
   '''

   notes = scale(6)
   beginning = notes[:2]
   middle = notes[2:4]
   end = notes[4:]

   t = Staff(beginning + end)
   p = Beam(t[ : ])

   r'''
   \new Staff {
           c'8 [
           d'8
           g'8
           a'8 ]
   }
   '''

   t[2:2] = middle
   p[2:2] = middle

   r'''
   \new Staff {
           c'8 [
           d'8
           e'8
           f'8
           g'8
           a'8 ]
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8 ]\n}"
   assert check(t)


def test_container_setitem_04( ):
   '''
   Containers set a single leaf over a sequence of leaves correctly.
   Spanners set a single leaf over a sequence of leaves correctly.
   '''

   t = Staff(scale(4))
   p = Beam(t[ : ])
   note = Note(12, (1, 8))
   t[1:3] = [note]
   p[1:3] = [note]

   r'''
   \new Staff {
           c'8 [
           c''8
           f'8 ]
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\tc''8\n\tf'8 ]\n}"
   assert check(t)


def test_container_setitem_05( ):
   '''
   Containers set a sequence of leaves over a sequence of leaves correctly.
   Spanners set a sequence of leaves over a sequence of leaves correctly.
   '''

   t = Staff(scale(4))
   p = Beam(t[ : ])
   notes = [Note(11, (1, 8)), Note(9, (1, 8)), Note(7, (1, 8))]
   t[1:3] = notes
   p[1:3] = notes

   r'''
   \new Staff {
           c'8 [
           b'8
           a'8
           g'8
           f'8 ]
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\tb'8\n\ta'8\n\tg'8\n\tf'8 ]\n}"
   assert check(t)


def test_container_setitem_06( ):
   '''Container magic.'''
   
   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Staff {
           {
                   c'8 [
                   d'8
           }
           {
                   e'8
                   f'8 ]
           }
   }
   '''

   sequential = t[0]
   t[0:1] = sequential.leaves

   r'''
   \new Staff {
           c'8 [
           d'8
           {
                   e'8
                   f'8 ]
           }
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
   assert check(t)
   assert len(sequential) == 0


def test_container_setitem_07( ):
   '''Container magic.'''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Staff {
           {
                   c'8 [
                   d'8
           }
           {
                   e'8
                   f'8 ]
           }
   }
   '''

   t[0:0] = [t[0][0]]

   r'''
   \new Staff {
           c'8 [
           {
                   d'8
           }
           {
                   e'8
                   f'8 ]
           }
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\t{\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"
   assert check(t)


def test_container_setitem_08( ):
   '''Container magic.'''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Staff {
           {
                   c'8 [
                   d'8
           }
           {
                   e'8
                   f'8 ]
           }
   }
   '''

   t[0:0] = t[0][:]

   r'''
   \new Staff {
           c'8 [
           d'8
           {
           }
           {
                   e'8
                   f'8 ]
           }
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\t{\n\t}\n\t{\n\t\te'8\n\t\tf'8 ]\n\t}\n}"


def test_container_setitem_09( ):
   '''Container magic.'''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Staff {
           {
                   c'8 [
                   d'8
           }
           {
                   e'8
                   f'8 ]
           }
   }
   '''

   sequential = t[0]
   t[0:0] = sequential[:]
   sequential[0:0] = t[-1][0:1]
   
   r'''
   \new Staff {
           c'8 [
           d'8
           {
                   e'8
           }
           {
                   f'8 ]
           }
   }
   '''
   
   assert t.format == "\\new Staff {\n\tc'8 [\n\td'8\n\t{\n\t\te'8\n\t}\n\t{\n\t\tf'8 ]\n\t}\n}"
   assert check(t)


def test_container_setitem_10( ):
   '''Container magic.'''

   t = Staff(Sequential(run(2)) * 2)
   diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Staff {
           {
                   c'8 [
                   d'8
           }
           {
                   e'8
                   f'8 ]
           }
   }
   '''

   t[0:0] = [t[0][0]]
   t[len(t):len(t)] = [t[-1][-1]]
   
   r'''
   \new Staff {
           c'8 [
           {
                   d'8
           }
           {
                   e'8
           }
           f'8 ]
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 [\n\t{\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t}\n\tf'8 ]\n}"
   assert check(t)
