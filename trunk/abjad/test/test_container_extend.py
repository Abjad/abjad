from abjad import *

def test_container_extend_01( ):
   '''Filled Container can extend from list of Leafs.'''
   t = Voice(Note(1, (1, 4))*4)
   t.extend(Note(1, (1, 4))*4)
   assert len(t) == 8

def test_container_extend_02( ):
   '''Filled Container can extend from another filled Container of Leafs.'''
   t = Voice(Note(1, (1, 4))*4)
   t.extend(Voice(Note(1, (1, 4))*4))
   assert len(t) == 8

def test_container_extend_03( ):
   '''Filled Container can extend from an empty list.'''
   t = Voice(Note(1, (1, 4))*4)
   t.extend([ ])
   assert len(t) == 4

def test_container_extend_04( ):
   '''Filled Container can extend from an empty Container.'''
   t = Voice(Note(1, (1, 4))*4)
   t.extend(Voice([ ]))
   assert len(t) == 4

