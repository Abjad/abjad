from abjad import *


def test_instances_01( ):
   '''Use instances( ) to pick out notes.'''
   t = Staff([Note(0, (1, 8)), Rest((1, 8)),
      Note(0, (1, 8)), Rest((1, 8)),
      Note(0, (1, 8)), Rest((1, 8)),
      Note(0, (1, 8)), Rest((1, 8)),
      Note(0, (1, 8)), Rest((1, 8))])
   notes = instances(t, Note)
   assert isinstance(notes, list)
   assert len(notes) == 5
   #assert all([hasname(x, 'Note') for x in notes])
   assert all([isinstance(x, Note) for x in notes])


def test_instances_02( ):
   '''Use instances( ) to pick out rests.'''
   t = Staff([Note(0, (1, 8)), Rest((1, 8)),
      Note(0, (1, 8)), Rest((1, 8)),
      Note(0, (1, 8)), Rest((1, 8)),
      Note(0, (1, 8)), Rest((1, 8)),
      Note(0, (1, 8)), Rest((1, 8))])
   rests = instances(t, Rest)
   assert isinstance(rests, list)
   assert len(rests) == 5
   #assert all([hasname(x, 'Rest') for x in rests])
   assert all([isinstance(x, Rest) for x in rests])
