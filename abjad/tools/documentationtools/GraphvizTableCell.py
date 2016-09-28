# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TreeNode


class GraphvizTableCell(TreeNode):
    r'''A Graphviz table cell.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = (
        '_attributes',
        '_label',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        label=None,
        name=None,
        attributes=None,
        ):
        TreeNode.__init__(
            self,
            name=name,
            )
        self._label = label
        if attributes is not None:
            attributes = dict(attributes)
        self._attributes = attributes

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Get string representation of Graphviz table cell.

        Returns string.
        '''
        result = []
        attribute_string = self._attribute_string
        if attribute_string:
            result.append('<TD {}>'.format(attribute_string))
        else:
            result.append('<TD>')
        result.append(self.label or '')
        result.append('</TD>')
        result = ''.join(result)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_string(self):
        if not self.attributes:
            return ''
        result = []
        for key, value in sorted(self.attributes.items()):
            attribute = '{}="{}"'.format(key.upper(), str(value).upper())
            result.append(attribute)
        result = ' '.join(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        r'''Gets Graphviz table cell attribute dictionary.

        Returns dictionary.
        '''
        return self._attributes

    @property
    def label(self):
        r'''Gets the field label.
        '''
        return self._label
