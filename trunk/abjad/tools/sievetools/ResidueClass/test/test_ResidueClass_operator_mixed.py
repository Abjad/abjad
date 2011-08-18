from abjad.tools import sievetools
from abjad.tools.sievetools.ResidueClass import ResidueClass
from abjad.tools.sievetools.ResidueClassExpression import ResidueClassExpression
import py.test


RC = ResidueClass

def test_ResidueClass_operator_mixed_01():
    '''Mixed operators yield nested ResidueClassExpressions.'''

    rc1 = RC(4, 0)
    rc2 = RC(4, 1)
    rc3 = RC(3, 0)
    rc4 = RC(3, 1)

    rcsA = rc1 & rc2
    rcsB = rc3 | rc4
    t = rcsA ^ rcsB

    assert isinstance(t, ResidueClassExpression)
    assert t.operator == 'xor'
    assert len(t.rcs) == 2
    assert isinstance(t.rcs[0], ResidueClassExpression)
    assert t.rcs[0].operator == 'and'
    assert isinstance(t.rcs[1], ResidueClassExpression)
    assert t.rcs[1].operator == 'or'
    assert t.rcs[0] is rcsA
    assert t.rcs[1] is rcsB


def test_ResidueClass_operator_mixed_02():
    '''Mixed operators yield nested ResidueClassExpressions.
    ResidueClassExpressions with the same operator, merge.'''

    rc1 = RC(4, 0)
    rc2 = RC(4, 1)
    rc3 = RC(3, 0)
    rc4 = RC(3, 1)

    rcsA = rc1 & rc2
    rcsB = rc3 | rc4
    t = rcsA | rcsB

    assert isinstance(t, ResidueClassExpression)
    assert t.operator == 'or'
    assert len(t.rcs) == 3
    assert isinstance(t.rcs[0], ResidueClassExpression)
    assert t.rcs[0].operator == 'and'
    assert isinstance(t.rcs[1], RC)
    assert isinstance(t.rcs[2], RC)
    assert t.rcs[0] is rcsA
    assert t.rcs[1] is rc3
    assert t.rcs[2] is rc4


def test_ResidueClass_operator_mixed_03():
    '''Operators combined.'''

    t = (RC(2, 0) ^ RC(3, 0)) | RC(3,0)

    assert isinstance(t, ResidueClassExpression)
    assert len(t.rcs) == 2
    assert isinstance(t.rcs[0], ResidueClassExpression)
    assert t.rcs[0].operator == 'xor'
    assert isinstance(t.rcs[1], RC)
    assert t.get_boolean_train(6) == [1,0,1,1,1,0]
    assert t.get_congruent_bases(6) == [0,2,3,4,6]


def test_ResidueClass_operator_mixed_04():
    '''Operators combined.'''

    t = (RC(2, 0) ^ RC(3, 0)) | RC(3,0)

    assert isinstance(t, ResidueClassExpression)
    assert len(t.rcs) == 2
    assert isinstance(t.rcs[0], ResidueClassExpression)
    assert t.rcs[0].operator == 'xor'
    assert isinstance(t.rcs[1], RC)
    assert t.get_boolean_train(6) == [1,0,1,1,1,0]
    assert t.get_congruent_bases(6) == [0,2,3,4,6]
