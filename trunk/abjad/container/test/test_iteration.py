from abjad import *


### TEST ITERATE MUSIC ###

def test_iterate_music_01( ):
   t = Staff([
      Note(0, (1, 8)),
      FixedDurationTuplet((1, 8), Note(0, (1, 16)) * 3),
      Chord([2, 3, 4], (1, 4)),
      Rest((1, 8)),
      Rest((1, 8))])
   for x in t[:-1]:
      assert x.next
   for x in t[1:]:
      assert x.prev


### TEST ITERATE LEAVES ###

def test_iterate_leaves_02( ):
   t = Staff([
      Note(0, (1, 8)),
      FixedDurationTuplet((1, 8), Note(0, (1, 16)) * 3),
      Chord([2, 3, 4], (1, 4)),
      Rest((1, 8)),
      Rest((1, 8))])
   for l in t.leaves[:-1]:
      assert l.next
   for l in t[1:]:
      assert l.prev 


### TEST ITERATE AND CAST ###

def test_iterate_and_cast_01( ):
   '''Casting while iterating works fine inside containers;
      note that 'naked casting' works fine here;
      reassignment x = Rest(x) is not necessary.'''
   t = Staff(Note(0, (1, 16)) * 10)
   for i, x in enumerate(t.leaves):
      if i % 2 == 0:
         Rest(x)
   assert check(t)
   assert t.format == "\\new Staff {\n\tr16\n\tc'16\n\tr16\n\tc'16\n\tr16\n\tc'16\n\tr16\n\tc'16\n\tr16\n\tc'16\n}"
   for i, x in enumerate(t.leaves):
      if i % 2 == 0:
         assert isinstance(x, Rest)      
      else:
         assert isinstance(x, Note)

def test_iterate_and_cast_02( ):
   '''Casting while iterating works fine inside containers;
      note that 'naked casting' works fine here;
      reassignment x = Skip(x) is not necessary.'''
   t = Staff(Note(0, (1, 16)) * 10)
   for i, x in enumerate(t.leaves):
      if i % 2 == 0:
         Skip(x)
   assert check(t)
   assert t.format == "\\new Staff {\n\ts16\n\tc'16\n\ts16\n\tc'16\n\ts16\n\tc'16\n\ts16\n\tc'16\n\ts16\n\tc'16\n}"
   for i, x in enumerate(t.leaves):
      if i % 2 == 0:
         assert isinstance(x, Skip)      
      else:
         assert isinstance(x, Note)

def test_iterate_and_cast_03( ):
   '''Casting while iterating works fine inside containers;
      note that 'naked casting' works fine here;
      reassignment x = Chord(x) is not necessary.'''
   t = Staff(Note(0, (1, 16)) * 10)
   for i, x in enumerate(t.leaves):
      if i % 2 == 0:
         Chord(x)
   assert check(t)
   for i, x in enumerate(t.leaves):
      if i % 2 == 0:
         assert isinstance(x, Chord)      
      else:
         assert isinstance(x, Note)
   assert t.format == "\\new Staff {\n\t<c'>16\n\tc'16\n\t<c'>16\n\tc'16\n\t<c'>16\n\tc'16\n\t<c'>16\n\tc'16\n\t<c'>16\n\tc'16\n}"
