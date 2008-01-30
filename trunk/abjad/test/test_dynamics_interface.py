from abjad import *


def test_dynamics_interface_01( ):
   '''Dynamics default to no mark, no hairpin and no effective dynamic.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   assert repr(staff[0].dynamics) == '_DynamicsInterface( )'
   for note in staff:
      assert note.dynamics.mark is None
      assert note.dynamics.hairpin is None
      assert note.dynamics.effective is None
   '''
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


def test_dynamics_interface_02( ):
   '''Marks grant an effective dynamic to notes following after.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].dynamics = 'p'
   for i, note in enumerate(staff):
      if i == 0:
         assert note.dynamics.mark == 'p'
         assert note.dynamics.hairpin is None
         assert note.dynamics.effective is 'p'
      else:
         assert note.dynamics.mark is None
         assert note.dynamics.hairpin is None
         assert note.dynamics.effective is 'p'
   '''
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


def test_dynamics_interface_03( ):
   '''Explicit marks show up as explicit marks;
      the effective dynamic of hairpinned notes shows up
      as a string representation of the hairpin.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[ : 4])
   staff[0].dynamics = 'p'
   staff[3].dynamics = 'f'
   for i, note in enumerate(staff):
      if i == 0:
         assert note.dynamics.mark == 'p'
         assert isinstance(note.dynamics.hairpin, Crescendo)
         assert isinstance(note.dynamics.effective, Crescendo)
      elif i in (1, 2):
         assert note.dynamics.mark == None
         assert isinstance(note.dynamics.hairpin, Crescendo)
         assert isinstance(note.dynamics.effective, Crescendo)
      elif i == 3:
         assert note.dynamics.mark == 'f'
         assert isinstance(note.dynamics.hairpin, Crescendo)
         assert isinstance(note.dynamics.effective, Crescendo)
      else:
         assert note.dynamics.mark is None
         assert note.dynamics.hairpin is None
         assert note.dynamics.effective == 'f'
   '''
   \new Staff {
           c'8 \pX \<
           cs'8
           d'8
           ef'8 \fX
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_dynamics_interface_04( ):
   '''Hairpins with neither a start mark nor a stop mark
      grant no effective dynamic to notes following after.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[ : 4])
   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   for i, note in enumerate(staff):
      if i in range(4):
         assert note.dynamics.mark is None
         assert isinstance(note.dynamics.hairpin, Crescendo)
         assert isinstance(note.dynamics.effective, Crescendo)
      else:
         assert note.dynamics.mark is None
         assert note.dynamics.hairpin is None
         assert note.dynamics.effective is None
   '''
   \new Staff {
           c'8 \<
           cs'8
           d'8
           ef'8 \!
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_dynamics_interface_05( ):
   '''Hairpins marked with a start mark but without a stop mark
      grant no effective dynamic to notes following after.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[ : 4])
   staff[0].dynamics = 'p'
   assert staff.format == "\\new Staff {\n\tc'8 \\pX \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   for i, note in enumerate(staff):
      if i == 0:
         assert note.dynamics.mark is 'p'
         assert isinstance(note.dynamics.hairpin, Crescendo)
         assert isinstance(note.dynamics.effective, Crescendo)
      elif i in (1, 2, 3):
         assert note.dynamics.mark is None
         assert isinstance(note.dynamics.hairpin, Crescendo)
         assert isinstance(note.dynamics.effective, Crescendo)
      else:
         assert note.dynamics.mark is None
         assert note.dynamics.hairpin is None
         assert note.dynamics.effective is None
   '''
   \new Staff {
           c'8 \pX \<
           cs'8
           d'8
           ef'8 \!
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_dynamics_interface_06( ):
   '''Hairpins with a stop mark grant an effective dynamic
      to notes following after.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[ : 4])
   staff[3].dynamics = 'f'
   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\fX\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   for i, note in enumerate(staff):
      if i in (0, 1, 2):
         assert note.dynamics.mark is None
         assert isinstance(note.dynamics.hairpin, Crescendo)
         assert isinstance(note.dynamics.effective, Crescendo)
      elif i == 3:
         assert note.dynamics.mark == 'f'
         assert isinstance(note.dynamics.hairpin, Crescendo)
         assert isinstance(note.dynamics.effective, Crescendo)
      else:
         assert note.dynamics.mark is None
         assert note.dynamics.hairpin is None
         assert note.dynamics.effective == 'f'
   '''
   \new Staff {
           c'8 \<
           cs'8
           d'8
           ef'8 \fX
           e'8
           f'8
           fs'8
           g'8
   }
   '''
