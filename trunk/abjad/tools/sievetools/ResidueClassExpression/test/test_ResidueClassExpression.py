from abjad.tools import sievetools
from abjad.tools.sievetools.ResidueClass import ResidueClass
from abjad.tools.sievetools.ResidueClassExpression import ResidueClassExpression
import py.test

RC = ResidueClass
# OR #

def test_ResidueClassExpression_01():
    '''boolean operator defaults to OR.'''

    t = ResidueClassExpression([RC(2, 0), RC(3, 0)])

    assert t.operator == 'or'


def test_ResidueClassExpression_02():

    t = ResidueClassExpression([RC(2, 0), RC(3, 0)])

    assert t.get_boolean_train(6) == [1,0,1,1,1,0]
    assert t.get_congruent_bases(6) == [0,2,3,4,6]


def test_ResidueClassExpression_03():

    t = ResidueClassExpression([RC(2, 1), RC(3, 0)])

    assert t.get_boolean_train(6) == [1,1,0,1,0,1]
    assert t.get_congruent_bases(6) == [0,1,3,5,6]


# AND #

def test_ResidueClassExpression_04():

    t = ResidueClassExpression([RC(2, 0), RC(3, 0)], 'and')

    assert t.operator == 'and'
    assert t.get_boolean_train(6) == [1,0,0,0,0,0]
    assert t.get_congruent_bases(6) == [0, 6]


def test_ResidueClassExpression_05():

    t = ResidueClassExpression([RC(2, 1), RC(3, 0)], 'and')

    assert t.get_boolean_train(6) == [0,0,0,1,0,0]
    assert t.get_congruent_bases(6) == [3]


# XOR #

def test_ResidueClassExpression_06():

    t = ResidueClassExpression([RC(2, 0), RC(3, 0)], 'xor')

    assert t.operator == 'xor'
    assert t.get_boolean_train(6) == [0,0,1,1,1,0]
    assert t.get_congruent_bases(6) == [2,3,4]


def test_ResidueClassExpression_07():

    t = ResidueClassExpression([RC(2, 1), RC(3, 0)], 'xor')

    assert t.get_boolean_train(6) == [1,1,0,0,0,1]
    assert t.get_congruent_bases(6) == [0,1,5,6]
