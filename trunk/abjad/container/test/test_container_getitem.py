from abjad import *
import py.test


def test_container_getitem_01( ):
   '''Get one container component with positive index.'''

   notes = scale(4)
   t = Voice(notes)

   assert t[0] is notes[0]
   assert t[1] is notes[1]
   assert t[2] is notes[2]
   assert t[3] is notes[3]


def test_container_getitem_02( ):
   '''Get one container component with negative index.'''

   notes = scale(4)
   t = Voice(notes)
   
   assert t[-1] is notes[3]
   assert t[-2] is notes[2]
   assert t[-3] is notes[1]
   assert t[-4] is notes[0]


def test_container_getitem_03( ):
   '''Get slice from container.'''

   notes = scale(4)
   t = Voice(notes)

   assert t[:1] == notes[:1]
   assert t[:2] == notes[:2]
   assert t[:3] == notes[:3]
   assert t[:4] == notes[:4]


def test_container_getitem_04( ):
   '''Bad index raises IndexError.'''

   t = Voice(scale(4))

   assert py.test.raises(IndexError, 't[99]')
