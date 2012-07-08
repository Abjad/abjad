from abc import abstractmethod
from abjad.tools import abctools
from collections import OrderedDict


class QSchemaItem(tuple, abctools.ImmutableAbjadObject):
    '''`QSchemaItem` represents a change of state in the timeline of a quantization process.

    `QSchemaItem` is abstract and immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    @abstractmethod
    def __new__(klass):
        raise Exception

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        'Return self as a plain tuple.  Used by copy and pickle.'
        return tuple(self)

    def __repr__(self):
        pieces = self._get_tools_package_qualified_keyword_argument_repr_pieces()
        if pieces:
            result = ['{}('.format(self._class_name)]
            result.extend(self._get_tools_package_qualified_keyword_argument_repr_pieces())
            result.append('\t)')
            return '\n'.join(result)
        return '{}()'.format(self._class_name)

    ### SPECIAL PROPERTIES ###

    @property
    def __dict__(self):
        return OrderedDict(zip(self._fields, self))

