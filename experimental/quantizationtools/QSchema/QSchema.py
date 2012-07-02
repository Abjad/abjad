from abjad.tools import abctools
from abjad.tools import datastructuretools
from abjad.tools import sequencetools
from experimental.quantizationtools.QSchemaEntry import QSchemaEntry
from experimental.quantizationtools.QTarget import QTarget
import copy


class QSchema(abctools.AbjadObject):
    '''The schema for a quantization run.'''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_items',)

    ### INITIALIZER ###

    def __init__(self, *args):
        if 1 == len(args) and isinstance(args[0], type(self)):
            items = copy.copy(args[0].items)

        elif 1 == len(args) and isinstance(args[0], dict):
            items = args[0]
            minimum = min(items)
            if minimum != 0:
                items = [(key - minimum, value) for key, value in items.iteritems()]
            items = datastructuretools.ImmutableDictionary(items)

        elif sequencetools.all_are_pairs_of_types(args, int, QSchemaEntry):
            items = dict(args)
            minimum = min(items)
            if minimum != 0:
                items = [(key - minimum, value) for key, value in items.iteritems()]
            items = datastructuretools.ImmutableDictionary(items)
            
        elif all([isinstance(x, QSchemaEntry) for x in args]):
            args = [(i, x) for i, x in enumerate(args)]
            items = datastructuretools.ImmutableDictionary(args)

        self._items = items

    ### SPECIAL METHODS ###

    def __call__(self):
        return QTarget(self)

    def __repr__(self):
        return '\n'.join(self._get_tools_package_qualified_repr_pieces())

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def items(self):
        return self._items

    ### PRIVATE METHODS ###

    def _get_tools_package_qualified_repr_pieces(self):
        if not len(self.items):
            return ['{}()'.format(self._tools_package_qualified_class_name)]

        result = ['{}({{'.format(self._tools_package_qualified_class_name)]
        for key, value in sorted(self.items.items()):
            value_repr = value._get_tools_package_qualified_repr_pieces()
            result.append('\t{}: {}'.format(key, value_repr[0]))
            result.extend(['\t' + x for x in value_repr[1:-1]])
            result.append('\t{},'.format(value_repr[-1]))
        result.append('\t})')
        return result


