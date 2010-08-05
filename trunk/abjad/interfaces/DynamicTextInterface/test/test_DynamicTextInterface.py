from abjad import *


def test_DynamicTextInterface_01( ):
   '''Dynamics default to no mark, no hairpin and no effective dynamic.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])

   r'''
   \new Staff {
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''

   for note in staff:
      assert note.dynamics.mark is None
      assert note.dynamics.effective is None
      #assert notnote.dynamics.spanner is None
      assert not note.dynamics.spanned


def test_DynamicTextInterface_02( ):
   '''Marks grant an effective dynamic to notes following after.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].dynamics.mark = 'p'
   for i, note in enumerate(staff):
      if i == 0:
         assert note.dynamics.mark == 'p'
         #assert note.dynamics.spanner is None
         assert not note.dynamics.spanned
         assert note.dynamics.effective is 'p'
      else:
         assert note.dynamics.mark is None
         #assert note.dynamics.spanner is None
         assert not note.dynamics.spanned
         assert note.dynamics.effective is 'p'
   r'''
   \new Staff {
           c'8 \pX
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


#def test_DynamicTextInterface_03( ):
#   '''Explicit marks show up as explicit marks;
#      the effective dynamic of hairpinned notes shows up
#      as a string representation of the hairpin.'''
#   staff = Staff([Note(n, (1, 8)) for n in range(8)])
#   Crescendo(staff[ : 4])
#   staff[0].dynamics.mark = 'p'
#   staff[3].dynamics.mark = 'f'
#   for i, note in enumerate(staff):
#      if i == 0:
#         assert note.dynamics.mark == 'p'
#         assert isinstance(note.dynamics.spanner, Crescendo)
#         assert isinstance(note.dynamics.effective, Crescendo)
#      elif i in (1, 2):
#         assert note.dynamics.mark == None
#         assert isinstance(note.dynamics.spanner, Crescendo)
#         assert isinstance(note.dynamics.effective, Crescendo)
#      elif i == 3:
#         assert note.dynamics.mark == 'f'
#         assert isinstance(note.dynamics.spanner, Crescendo)
#         assert isinstance(note.dynamics.effective, Crescendo)
#      else:
#         assert note.dynamics.mark is None
#         assert note.dynamics.spanner is None
#         assert note.dynamics.effective == 'f'
#   '''
#   \new Staff {
#           c'8 \pX \<
#           cs'8
#           d'8
#           ef'8 \fX
#           e'8
#           f'8
#           fs'8
#           g'8
#   }
#   '''
#
#
#def test_DynamicTextInterface_04( ):
#   '''Hairpins with neither a start mark nor a stop mark
#      grant no effective dynamic to notes following after.'''
#   staff = Staff([Note(n, (1, 8)) for n in range(8)])
#   Crescendo(staff[ : 4])
#   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   for i, note in enumerate(staff):
#      if i in range(4):
#         assert note.dynamics.mark is None
#         assert isinstance(note.dynamics.spanner, Crescendo)
#         assert isinstance(note.dynamics.effective, Crescendo)
#      else:
#         assert note.dynamics.mark is None
#         assert note.dynamics.spanner is None
#         assert note.dynamics.effective is None
#   '''
#   \new Staff {
#           c'8 \<
#           cs'8
#           d'8
#           ef'8 \!
#           e'8
#           f'8
#           fs'8
#           g'8
#   }
#   '''
#
#
#def test_DynamicTextInterface_05( ):
#   '''Hairpins marked with a start mark but without a stop mark
#      grant no effective dynamic to notes following after.'''
#   staff = Staff([Note(n, (1, 8)) for n in range(8)])
#   Crescendo(staff[ : 4])
#   staff[0].dynamics.mark = 'p'
#   assert staff.format == "\\new Staff {\n\tc'8 \\pX \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   for i, note in enumerate(staff):
#      if i == 0:
#         assert note.dynamics.mark is 'p'
#         assert isinstance(note.dynamics.spanner, Crescendo)
#         assert isinstance(note.dynamics.effective, Crescendo)
#      elif i in (1, 2, 3):
#         assert note.dynamics.mark is None
#         assert isinstance(note.dynamics.spanner, Crescendo)
#         assert isinstance(note.dynamics.effective, Crescendo)
#      else:
#         assert note.dynamics.mark is None
#         assert note.dynamics.spanner is None
#         assert note.dynamics.effective is None
#   '''
#   \new Staff {
#           c'8 \pX \<
#           cs'8
#           d'8
#           ef'8 \!
#           e'8
#           f'8
#           fs'8
#           g'8
#   }
#   '''
#
#
#def test_DynamicTextInterface_06( ):
#   '''Hairpins with a stop mark grant an effective dynamic
#      to notes following after.'''
#   staff = Staff([Note(n, (1, 8)) for n in range(8)])
#   Crescendo(staff[ : 4])
#   staff[3].dynamics.mark = 'f'
#   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\fX\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
#   for i, note in enumerate(staff):
#      if i in (0, 1, 2):
#         assert note.dynamics.mark is None
#         assert isinstance(note.dynamics.spanner, Crescendo)
#         assert isinstance(note.dynamics.effective, Crescendo)
#      elif i == 3:
#         assert note.dynamics.mark == 'f'
#         assert isinstance(note.dynamics.spanner, Crescendo)
#         assert isinstance(note.dynamics.effective, Crescendo)
#      else:
#         assert note.dynamics.mark is None
#         assert note.dynamics.spanner is None
#         assert note.dynamics.effective == 'f'
#   '''
#   \new Staff {
#           c'8 \<
#           cs'8
#           d'8
#           ef'8 \fX
#           e'8
#           f'8
#           fs'8
#           g'8
#   }
#   '''


def test_DynamicTextInterface_07( ):
   '''Dynamics interface maps to DynamicText.'''
   t = Note(0, (1, 4))
   t.dynamics.self_alignment_X = -0.5
   assert t.format == "\\once \\override DynamicText #'self-alignment-X = #-0.5\nc'4"
   r'''
   \once \override DynamicText #'self-alignment-X = #-0.5
   c'4
   '''


def test_DynamicTextInterface_08( ):
   '''Dynamics interface implements first, last, only.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   #Crescendo(t)
   Crescendo(t.leaves)
   assert t[0].dynamics.first
   assert t[-1].dynamics.last
   assert not t[0].dynamics.only
   r'''
   \new Staff {
           c'8 \<
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8 \!
   }
   '''
