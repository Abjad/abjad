from abjad.mixins._MutableAbjadObject import _MutableAbjadObject
from abjad.tools.contexttools.ClefMark import ClefMark


class ClefMarkInventory(list, _MutableAbjadObject):
    '''.. versionadded:: 2.8

    Abjad model of an ordered list of clefs::

        abjad> inventory = contexttools.ClefMarkInventory(['treble', 'bass'])

    ::

        abjad> inventory
        ClefMarkInventory([ClefMark('treble'), ClefMark('bass')])

    ::

        abjad> 'treble' in inventory
        True

    ::

        abjad> contexttools.ClefMark('treble') in inventory
        True

    ::

        abjad> 'alto' in inventory
        False

    Clef mark inventories inherit from list and are mutable.
    '''

    def __init__(self, tokens=None):
        list.__init__(self)
        tokens = tokens or []
        elements = []
        for token in tokens:
            elements.append(ClefMark(token))
        self.extend(elements)

    ### OVERLOADS ###

    def __contains__(self, token):
        try:
            element = ClefMark(token)
            return list.__contains__(self, element)
        except ValueError:
            return False

    def __repr__(self):
        return '{}({})'.format(self.class_name, list.__repr__(self))

    ### PRIVATE ATTRIBUTES ###

    @property
    def _class_name_with_tools_package(self):
        return '{}.{}'.format(self._tools_package, self.class_name)

    @property
    def _contents_repr_with_tools_package(self):
        part_reprs = []
        for element in self:
            part_repr = getattr(element, '_repr_with_tools_package', repr(element))
            part_reprs.append(part_repr)
        return ', '.join(part_reprs)

    @property
    def _repr_with_tools_package(self):
        return '{}([{}])'.format(
            self._class_name_with_tools_package, self._contents_repr_with_tools_package)

    @property
    def _tools_package(self):
        for part in reversed(self.__module__.split('.')):
            if not part == self.class_name:
                return part

    ### PUBLIC METHODS ###

    def append(self, token):
        element = ClefMark(token)
        list.append(self, element)

    def extend(self, tokens):
        elements = []
        for token in tokens:
            elements.append(ClefMark(token))
        list.extend(self, elements)
