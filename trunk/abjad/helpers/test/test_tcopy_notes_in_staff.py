from abjad import *


def test_tcopy_notes_in_staff_01( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[0 : 1])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], Note)
   assert u[0].pitch.number == t[0].pitch.number
   assert id(u[0]) is not id(t[0])
   assert u[0]._parent == u


def test_tcopy_notes_in_staff_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[1 : 2])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], Note)
   assert u[0].pitch.number == t[1].pitch.number
   assert id(u[0]) is not id(t[1])
   assert u[0]._parent == u
   

def test_tcopy_notes_in_staff_03( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[-1 :])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], Note)
   assert u[0].pitch.number == t[-1].pitch.number
   assert id(u[0]) is not id(t[-1])
   assert u[0]._parent == u
   

def test_tcopy_notes_in_staff_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[-2:-1])
   assert isinstance(u, Staff)
   assert len(u) == 1
   assert isinstance(u[0], Note)
   assert u[0].pitch.number == t[-2].pitch.number
   assert id(u[0]) is not id(t[-2])
   assert u[0]._parent == u


def test_tcopy_notes_in_staff_05( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[0:3])
   assert isinstance(u, Staff)
   assert len(u) == 3
   for i, x in enumerate(u):
      assert x.pitch.number == t[i].pitch.number
      assert id(x) is not id(t[i])
   assert check(u)


def test_tcopy_notes_in_staff_06( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   u = tcopy(t[1:7])
   assert isinstance(u, Staff)
   assert len(u) == 6
   for i, x in enumerate(u):
      j = i + 1
      assert x.pitch.number == t[j].pitch.number
      assert id(x) is not id(t[j])
   assert check(u)
