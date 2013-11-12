# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class Specifier(AbjadObject):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, description=None, custom_identifier=None, source=None):
        self.description = description
        self.custom_identifier = custom_identifier
        self.source = source

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if self is expr:
            return True
        if isinstance(expr, type(self)):
            if self._positional_argument_values == \
                expr._positional_argument_values:
                if self._keyword_argument_name_value_strings == \
                    expr._keyword_argument_name_value_strings:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats specifier.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        if format_specification in ('', 'storage'):
            return self._tools_package_qualified_indented_repr
        return str(self)

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _one_line_menuing_summary(self):
        pass
