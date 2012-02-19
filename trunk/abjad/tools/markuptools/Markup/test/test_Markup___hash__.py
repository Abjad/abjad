from abjad.tools.markuptools import Markup


def test_Markup___hash___01():
    '''The hashes of two Markup instances compare equally if the instances compare equally.'''
    one = Markup('foo')
    two = Markup('foo')
    three = Markup('bar')
    assert one == two
    assert hash(one) == hash(two)
    assert one != three
    assert hash(one) != hash(three)
