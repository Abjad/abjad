from abjad import *


def test_breaks_interface_01( ):
   '''Line break at closing of nonempty container.'''

   t = Staff(macros.scale(4))
   t.breaks.line = True

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
           \break
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\break\n}"


def test_breaks_interface_02( ):
   '''Page break at closing of nonempty container.'''

   t = Staff(macros.scale(4))
   t.breaks.page = True

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
           \pageBreak
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n\t\\pageBreak\n}"


def test_breaks_interface_03( ):
   '''Both line and page break on nonempty container.'''

   t = Staff(Note(0, (1, 4)) * 4)
   t.breaks.line = True
   t.breaks.page = True

   r'''
   \new Staff {
      c'4
      c'4
      c'4
      c'4
      \break
      \pageBreak
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\t\\break\n\t\\pageBreak\n}"


def test_breaks_interface_04( ):
   '''Line break on leaf.'''

   t = Note(0, (1, 4))
   t.breaks.line = True

   r'''
   c'4
   \break
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "c'4\n\\break"


def test_breaks_interface_05( ):
   '''Page break on leaf.'''

   t = Note(0, (1, 4))
   t.breaks.page = True

   r'''
   c'4
   \pageBreak
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "c'4\n\\pageBreak"


def test_breaks_interface_06( ):
   '''Both line and page break on leaf.'''

   t = Note(0, (1, 4))
   t.breaks.line = True
   t.breaks.page = True

   r'''
   c'4
   \break
   \pageBreak
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "c'4\n\\break\n\\pageBreak"


def test_breaks_interface_07( ):
   '''The clear( ) method clears both line and page breaks
      on containers.'''

   t = Staff(Note(0, (1, 4)) * 4)
   t.breaks.line = True
   t.breaks.page = True
   t.breaks.clear( )

   r'''
   \new Staff {
      c'4
      c'4
      c'4
      c'4
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"

def test_breaks_interface_08( ):
   '''The clear( ) method clears both line and page breaks
      on leaves.'''

   t = Note(0, (1, 4))
   t.breaks.line = True
   t.breaks.page = True
   t.breaks.clear( )

   assert t.format == "c'4"


def test_breaks_interface_09( ):
   '''BreaksInterface returns True when 'line' is True.'''

   t = Note(0, (1, 4))
   t.breaks.line = True

   assert bool(t.breaks)
   

def test_breaks_interface_10( ):
   '''BreaksInterface returns True when 'page' is True.'''

   t = Note(0, (1, 4))
   t.breaks.page = True

   assert bool(t.breaks)
   

def test_breaks_interface_11( ):
   '''BreaksInterface returns True when both
      'line' and 'page' are True.'''

   t = Note(0, (1, 4))
   t.breaks.line = True
   t.breaks.page = True

   assert bool(t.breaks)
   

def test_breaks_interface_12( ):
   '''BreaksInterface returns False when neither
      'line' nor 'page' are True.'''

   t = Note(0, (1, 4))

   assert not bool(t.breaks)
