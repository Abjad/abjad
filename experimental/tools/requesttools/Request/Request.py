import abc
import copy
from abjad.tools import datastructuretools
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.tools import helpertools


class Request(AbjadObject):
    r'''.. versionadded:: 1.0

    Base class from which other request classes inherit.

    Requests function as setting sources.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    attributes = helpertools.AttributeNameEnumeration()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, modifications=None, index=None, count=None, reverse=None, rotation=None):
        assert isinstance(index, (int, type(None))), repr(index)
        assert isinstance(count, (int, type(None))), repr(count)
        assert isinstance(reverse, (bool, type(None))), repr(reverse)
        assert isinstance(rotation, (int, type(None))), repr(rotation)
        modifications = modifications or []
        self._modifications = datastructuretools.ObjectInventory(modifications)
        self._index = index
        self._count = count
        self._reverse = reverse
        self._rotation = rotation

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _keyword_argument_name_value_strings(self):
        result = AbjadObject._keyword_argument_name_value_strings.fget(self)
        if 'modifications=ObjectInventory([])' in result:
            result = list(result)
            result.remove('modifications=ObjectInventory([])')
        return tuple(result)

    ### PRIVATE METHODS ###

    def _clone(self):
        return copy.deepcopy(self)

    def _get_tools_package_qualified_keyword_argument_repr_pieces(self, is_indented=True):
        '''Do not show empty modifications list.
        '''
        filtered_result = []
        result = AbjadObject._get_tools_package_qualified_keyword_argument_repr_pieces(
            self, is_indented=is_indented)
        for string in result:
            if not 'modifications=datastructuretools.ObjectInventory([])' in string:
                filtered_result.append(string)
        return filtered_result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def count(self):
        return self._count

    @property
    def index(self):
        return self._index

    @property
    def modifications(self):
        return self._modifications

    @property
    def reverse(self):
        return self._reverse

    @property
    def rotation(self):
        return self._rotation

    ### PUBLIC METHODS ###

    def rotate(self, index):
        '''Return copy of request with appended modification.
        '''
        modification = 'target.rotate({!r})'.format(index)    
        result = self._clone()
        result.modifications.append(modification)
        return result
