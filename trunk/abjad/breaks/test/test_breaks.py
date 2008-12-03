from abjad import *


def test_breaks_01( ):
   '''Line break on nonempty container.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.breaks.line = True
   assert t.format == "\\new Staff {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\t\\break\n}"
   r'''
   \new Staff {
      c'4
      c'4
      c'4
      c'4
      \break
   }
   '''


def test_breaks_02( ):
   '''Page break on nonempty container.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.breaks.page = True
   assert t.format == "\\new Staff {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\t\\pageBreak\n}"
   r'''
   \new Staff {
      c'4
      c'4
      c'4
      c'4
      \pageBreak
   }
   '''


def test_breaks_03( ):
   '''Both line and page break on nonempty container.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.breaks.line = True
   t.breaks.page = True
   assert t.format == "\\new Staff {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n\t\\break\n\t\\pageBreak\n}"
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


def test_breaks_04( ):
   '''Line break on leaf.'''
   t = Note(0, (1, 4))
   t.breaks.line = True
   assert t.format == "c'4\n\\break"
   r'''
   c'4
   \break
   '''


def test_breaks_05( ):
   '''Page break on leaf.'''
   t = Note(0, (1, 4))
   t.breaks.page = True
   assert t.format == "c'4\n\\pageBreak"
   r'''
   c'4
   \pageBreak
   '''


def test_breaks_06( ):
   '''Both line and page break on leaf.'''
   t = Note(0, (1, 4))
   t.breaks.line = True
   t.breaks.page = True
   assert t.format == "c'4\n\\break\n\\pageBreak"
   r'''
   c'4
   \break
   \pageBreak
   '''


def test_breaks_07( ):
   '''The clear( ) method clears both line and page breaks
      on containers.'''
   t = Staff(Note(0, (1, 4)) * 4)
   t.breaks.line = True
   t.breaks.page = True
   t.breaks.clear( )
   assert t.format == "\\new Staff {\n\tc'4\n\tc'4\n\tc'4\n\tc'4\n}"
   r'''
   \new Staff {
      c'4
      c'4
      c'4
      c'4
   }
   '''

def test_breaks_08( ):
   '''The clear( ) method clears both line and page breaks
      on leaves.'''
   t = Note(0, (1, 4))
   t.breaks.line = True
   t.breaks.page = True
   t.breaks.clear( )
   assert t.format == "c'4"


def test_breaks_09( ):
   '''_BreaksInterface returns True when 'line' is True.'''
   t = Note(0, (1, 4))
   t.breaks.line = True
   assert bool(t.breaks)
   

def test_breaks_10( ):
   '''_BreaksInterface returns True when 'page' is True.'''
   t = Note(0, (1, 4))
   t.breaks.page = True
   assert bool(t.breaks)
   

def test_breaks_11( ):
   '''_BreaksInterface returns True when both
      'line' and 'page' are True.'''
   t = Note(0, (1, 4))
   t.breaks.line = True
   t.breaks.page = True
   assert bool(t.breaks)
   

def test_breaks_12( ):
   '''_BreaksInterface returns False when neither
      'line' nor 'page' are True.'''
   t = Note(0, (1, 4))
   assert not bool(t.breaks)
