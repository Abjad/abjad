import abc
from abjad.tools import iotools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Specifier(AbjadObject):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, description=None, name=None, source=None):
        self.description = description
        self.name = name
        self.source = source

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if self is expr:
            return True
        if isinstance(expr, type(self)):
            if self._positional_argument_values == expr._positional_argument_values:
                if self._keyword_argument_name_value_strings == expr._keyword_argument_name_value_strings:
                    return True
        return False

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def one_line_menuing_summary(self):
        pass
