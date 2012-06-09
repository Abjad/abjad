from experimental.specificationtools.Directive import Directive


def test_Directive___init___01():
    '''Init by hand.
    '''

    directive = Directive(None, 'time_signatures', [(4, 8), (3, 8)])
    assert isinstance(directive, Directive)


def test_Directive___init___02():
    '''Init from other directive.
    '''

    directive_1 = Directive(None, 'time_signatures', [(4, 8), (3, 8)], persistent=False, truncate=False)
    directive_2 = Directive(directive_1)

    assert isinstance(directive_1, Directive)
    assert isinstance(directive_2, Directive)
    assert not directive_1 is directive_2
    assert directive_1 == directive_2
