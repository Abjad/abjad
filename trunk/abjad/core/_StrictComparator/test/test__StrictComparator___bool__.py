from abjad import *

__doc__ = '''All Abjad objects should evaluate to True
    unless specifically implemented otherwise.

    You would think that, for example,

    if staff:
        whatever

    would execute for any value of staff.

    But this turns out not be true.
    Python's bool() function looks for
    any definition of __nonzero__ on an object;
    if not found, Python evaluates __len__;
    if not found, Python assumes an object is True.

    This is particulary important for containers
    that implement __len__: empty containers carry
    length zero and set bool() to False.

    What fixes this is defining __nonzero__ explicitly
    to True on all system objects.'''

def test__StrictComparator___bool___01():
    '''Leaves evaluate to True.'''
    assert bool(Note("c'4"))
    assert bool(Rest((1, 4)))
    assert bool(Chord([0, 2, 10], (1, 4)))
    assert bool(skiptools.Skip((1, 4)))


def test__StrictComparator___bool___02():
    '''Empty chords evaluate to True,
        even though they carry zero length.'''
    assert bool(Chord([], (1, 4)))



def test__StrictComparator___bool___03():
    '''Nonempty containers evaluate to True.'''
    assert bool(Staff(Note("c'4") * 4))
    assert bool(Voice(Note("c'4") * 4))
    assert bool(Container(Note("c'4") * 4))
    assert bool(tuplettools.FixedDurationTuplet(Duration(2, 4), Note("c'4") * 3))
    #assert bool(Tuplet(Fraction(2, 3), Note("c'4") * 3))
    assert bool(Tuplet(Fraction(2, 3), Note("c'4") * 3))


def test__StrictComparator___bool___04():
    '''Empty containers evaluate to True.'''
    assert bool(Staff([]))
    assert bool(Voice([]))
    assert bool(Container([]))
    assert bool(tuplettools.FixedDurationTuplet(Duration(2, 4), []))
    #assert bool(Tuplet(Fraction(2, 3), []))
    assert bool(Tuplet(Fraction(2, 3), []))
