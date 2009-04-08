from abjad import *


def test_update_interface_01( ):
   '''Newly instantiated notes are not current.'''

   t = Note(0, (1, 4))
   assert not t._update._current
   
   t.offset.score
   assert t._update._current
   

def test_update_interface_02( ):
   '''Newly instantiated containers are not current.'''

   t = Voice(scale(4))
   assert not t._update._current

   t[-1].offset.score
   assert t._update._current


def test_update_interface_03( ):
   '''Copied notes are not current.'''

   t = Note(0, (1, 4))
   t.offset.score
   new = clone_unspan([t])[0]
   assert not new._update._current


def test_update_interface_04( ):
   '''Copied containers are not current.'''

   t = Voice(scale(4))
   t[-1].offset.score
   new = clone_unspan([t])[0]
   assert not new._update._current


def test_update_interface_05( ):
   '''Container deletion marks all components in parentage for update.'''

   t = Voice(scale(4))
   t[-1].offset.score
   assert t._update._current

   del(t[1])
   assert not t._update._current


def test_update_interface_06( ):
   '''Container insert marks all components in parentage for update.'''

   t = Voice(scale(4))
   t[-1].offset.score
   assert t._update._current
   
   t.insert(1, Note(1, (1, 16)))
   assert not t._update._current


def test_update_interface_07( ):
   '''Container append marks components in parentage for update.'''

   t = Voice(scale(4))
   t[-1].offset.score
   assert t._update._current

   t.append(Note(7, (1, 8)))
   assert not t._update._current


def test_update_interface_08( ):
   '''Container extend marks components in parentage for update.'''

   t = Voice(scale(4))
   t[-1].offset.score
   assert t._update._current

   t.extend([Note(7, (1, 8)), Note(9, (1, 8))])
   assert not t._update._current


def test_update_interface_09( ):
   '''Container pop marks components in parentage for update.'''

   t = Voice(scale(4))
   t[-1].offset.score
   assert t._update._current

   t.pop( )
   assert not t._update._current


def test_update_interface_10( ):
   '''Container remove marks components in parentage for update.'''

   t = Voice(scale(4))
   t[-1].offset.score
   assert t._update._current

   t.remove(t[1])
   assert not t._update._current
