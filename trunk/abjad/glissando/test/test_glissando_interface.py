from abjad import *


def test_glissando_interface_01( ):
   '''Glissando interface tests nonzero.'''
   t = Note(0, (3, 64))
   assert not t.glissando
   t.glissando.set = True
   assert t.glissando


def test_glissando_interface_02( ):
   '''Glissando interface tests eq.'''
   t = Note(0, (3, 64))
   assert t.glissando.set == False
   t.glissando.set = True
   assert t.glissando.set == True


def test_glissando_interface_03( ):
   '''Glissando interface formats all but the last note.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Glissando(t.leaves[ : 4])
   assert t.format == "\\new Staff {\n\tc'8 \\glissando\n\tcs'8 \\glissando\n\td'8 \\glissando\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           c'8 \glissando
           cs'8 \glissando
           d'8 \glissando
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

def test_glissando_interface_04( ):
   '''Attributes format correcty.'''
   t = Note(0, (1,4))
   t.glissando.color = 'red'
   assert t.format == "\\once \\override Glissando #'color = #red\nc'4"
  

def test_glissando_interface_05( ):
   '''Clear deletes assigned attributes.'''
   t = Note(0, (1,4))
   t.glissando.color = 'red'
   assert t.format == "\\once \\override Glissando #'color = #red\nc'4"
   t.glissando.clear()
   assert t.format == "c'4"


