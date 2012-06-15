import py


def test_OrdinalConstant___builtins___01():

    assert Left < Center < Right
    assert Down < Up


def test_OrdinalConstant___builtins___02():

    assert py.test.raises(Exception, 'Down < Right')
