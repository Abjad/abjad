# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.specifiers.Specifier \
	import Specifier
from experimental import *


class ConcreteSpecifier(Specifier):
    @property
    def _one_line_menuing_summary(self):
        pass
    @property
    def _tools_package_name(self):
        return 'specialtools'


def test_Specifier___format___01():
    r'''No keywords.
    '''

    specifier = ConcreteSpecifier()

    assert repr(specifier) == 'ConcreteSpecifier()'
    assert format(specifier) == 'specialtools.ConcreteSpecifier()'


def test_Specifier___format___02():
    r'''With keywords.
    '''

    specifier = ConcreteSpecifier(name='foo')

    assert repr(specifier) == "ConcreteSpecifier(name='foo')"
    assert format(specifier) == "specialtools.ConcreteSpecifier(\n\tname='foo'\n\t)"
