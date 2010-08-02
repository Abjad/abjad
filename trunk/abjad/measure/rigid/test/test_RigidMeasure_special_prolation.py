from abjad import *


def test_RigidMeasure_special_prolation_01( ):
   '''Binary measures contribute trivially to contents prolation;
      works on a flat list of notes.'''
   t = RigidMeasure((4, 4), Note(0, (1, 4)) * 4)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 4)


def test_RigidMeasure_special_prolation_02( ):
   '''Binary measures contribute trivially to contents prolation;
      works on notes and tuplets together.'''
   t = RigidMeasure((4, 4), [
      Note(0, (1, 4)),
      FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3),
      Note(0, (1, 4))])
   assert t.leaves[0].duration.written == Rational(1, 4)
   assert t.leaves[0].duration.prolated == Rational(1, 4)
   assert t.leaves[1].duration.written == Rational(1, 4)
   assert t.leaves[1].duration.prolated == Rational(1, 6)


def test_RigidMeasure_special_prolation_03( ):
   '''Binary measures contribute trivially to contents prolation;
      works on notes and nested tuplets together.'''
   t = RigidMeasure((4, 4), [
      Note(0, (1, 4)),
      FixedDurationTuplet((2, 4), [
         FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3),
         Note(0, (1, 4))]),
      Note(0, (1, 4))])
   assert t.leaves[0].duration.written == Rational(1, 4)
   assert t.leaves[0].duration.prolated == Rational(1, 4)
   assert t.leaves[1].duration.written == Rational(1, 4)
   assert t.leaves[1].duration.prolated == Rational(1, 9)


def test_RigidMeasure_special_prolation_04( ):
   '''Nonbinary measures contribute nontrivially to contents prolation;
      works on a flat list of notes.'''
   t = RigidMeasure((4, 5), Note(0, (1, 4)) * 4)
   assert t[0].duration.written == Rational(1, 4)
   assert t[0].duration.prolated == Rational(1, 5)


def test_RigidMeasure_special_prolation_05( ):
   '''Nonbinary measures contribute trivially to contents prolation;
      works on notes and tuplets together.'''
   t = RigidMeasure((4, 5), [
      Note(0, (1, 4)),
      FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3),
      Note(0, (1, 4))])
   assert t.leaves[0].duration.written == Rational(1, 4)
   assert t.leaves[0].duration.prolated == Rational(1, 5)
   assert t.leaves[1].duration.written == Rational(1, 4)
   assert t.leaves[1].duration.prolated == Rational(2, 15)


def test_RigidMeasure_special_prolation_06( ):
   '''Nonbinary measures contribute nontrivially to contents prolation;
      works on notes and nested tuplets together.'''
   t = RigidMeasure((4, 5), [
      Note(0, (1, 4)),
      FixedDurationTuplet((2, 4), [
         FixedDurationTuplet((2, 4), Note(0, (1, 4)) * 3),
         Note(0, (1, 4))]),
      Note(0, (1, 4))])
   assert t.leaves[0].duration.written == Rational(1, 4)
   assert t.leaves[0].duration.prolated == Rational(1, 5)
   assert t.leaves[1].duration.written == Rational(1, 4)
   assert t.leaves[1].duration.prolated == Rational(4, 45)
