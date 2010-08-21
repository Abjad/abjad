from abjad import *


def test_Grace_parentage_01( ):
   '''Lone grace container carrier is none.
   '''

   t = gracetools.Grace(notetools.make_repeated_notes(4))
   assert t._carrier is None


def test_Grace_parentage_02( ):
   '''Grace containers bound to leaf do have parent.
   '''

   t = Note(1, (1, 4))
   #assert isinstance(t.grace.before, gracetools.Grace)
   #assert t.grace.before._carrier is t
   #assert t.grace.after._carrier is t
   assert isinstance(t.grace, gracetools.Grace)
   assert t.grace._carrier is t
   assert t.grace._carrier is t


def test_Grace_parentage_03( ):
   '''Grace containers bound to leaf have their correct carrier after assignment.
   '''

#   t = Note(1, (1, 4))
#   t.grace.after = Note(4, (1, 16))
#   t.grace.before = Note(4, (1, 16))
#   assert t.grace.after._carrier is t
#   assert t.grace.before._carrier is t
#   t.grace.after = gracetools.Grace(macros.scale(2))
#   t.grace.before = gracetools.Grace(macros.scale(2))
#   assert t.grace.after._carrier is t
#   assert t.grace.before._carrier is t
#   t.grace.after = None
#   t.grace.before = None
#   assert t.grace.after._carrier is t
#   assert t.grace.before._carrier is t

   t = Note(1, (1, 4))
   t.after_grace.append(Note(4, (1, 16)))
   t.grace.append(Note(4, (1, 16)))
   assert t.after_grace._carrier is t
   assert t.grace._carrier is t
   t.after_grace[:] = [ ]
   t.after_grace.extend(macros.scale(2))
   t.grace[:] = [ ]
   t.grace.extend(macros.scale(2))
   assert t.after_grace._carrier is t
   assert t.grace._carrier is t
   t.after_grace[:] = [ ]
   t.grace[:] = [ ]
   assert t.after_grace._carrier is t
   assert t.grace._carrier is t


def test_Grace_parentage_04( ):
   '''Grace containers bound to leaf have their correct carrier after leaf casting.
   '''

#   n = Note(1, (1, 4))
#   t = Rest(n)
#   assert isinstance(t, Rest)
#   assert t.grace.after._carrier is t
#   assert t.grace.before._carrier is t
#   t = Skip(n)
#   assert isinstance(t, Skip)
#   assert t.grace.after._carrier is t
#   assert t.grace.before._carrier is t
#   t = Chord(n)
#   assert isinstance(t, Chord)
#   assert t.grace.after._carrier is t
#   assert t.grace.before._carrier is t
#   t = Note(n)
#   assert isinstance(t, Note)
#   assert t.grace.after._carrier is t
#   assert t.grace.before._carrier is t

   n = Note(1, (1, 4))
   t = Rest(n)
   assert isinstance(t, Rest)
   assert t.after_grace._carrier is t
   assert t.grace._carrier is t
   t = Skip(n)
   assert isinstance(t, Skip)
   assert t.after_grace._carrier is t
   assert t.grace._carrier is t
   t = Chord(n)
   assert isinstance(t, Chord)
   assert t.after_grace._carrier is t
   assert t.grace._carrier is t
   t = Note(n)
   assert isinstance(t, Note)
   assert t.after_grace._carrier is t
   assert t.grace._carrier is t
