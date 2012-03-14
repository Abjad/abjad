from abjad.tools import abctools


def test_AbjadObject___repr___01():

    class Foo(abctools.AbjadObject):
        def __init__(self, x, y, flavor=None):
            tmp_1 = 'foo'
            self.x = x
            self.y = y
            self.flavor = flavor
            tmp_2 = 'bar'
        @property
        def _keyword_argument_names(self):
            return ('flavor', )
        @property
        def _mandatory_argument_values(self):
            return (self.x, self.y)

    assert repr(Foo(7, 8)) == 'Foo(7, 8)'
    assert repr(Foo(7, 8, 'cherry')) == "Foo(7, 8, flavor='cherry')"


def test_AbjadObject___repr___02():
    '''Repr suppresses class methods to avoid recursive repr.
    '''

    class Foo(abctools.AbjadObject):
        def __init__(self, x, y, helper=None):
            tmp_1 = 'foo'
            self.x = x
            self.y = y
            self.helper = helper or self.do_stuff
            tmp_2 = 'bar'
        def do_stuff(self):
            pass

    assert repr(Foo(7, 8)) == 'Foo(7, 8)'
