from experimental.tools.scoremanagertools.specifiers.Specifier import Specifier
from experimental import *


class ConcreteSpecifier(Specifier):
    @property
    def _tools_package_name(self):
        return 'specialtools'
    @property
    def one_line_menuing_summary(self):
        pass


def test_Specifier_format_01():
    '''No keywords.
    '''

    specifier = ConcreteSpecifier()

    assert repr(specifier) == 'ConcreteSpecifier()'
    assert specifier._storage_format == 'specialtools.ConcreteSpecifier()'


def test_Specifier_format_02():
    '''With keywords.
    '''

    specifier = ConcreteSpecifier(name='foo')

    assert repr(specifier) == "ConcreteSpecifier(name='foo')"
    assert specifier._storage_format == "specialtools.ConcreteSpecifier(\n\tname='foo'\n\t)"
