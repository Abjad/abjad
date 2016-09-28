# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools import TreeContainer


class GraphvizTable(TreeContainer):
    r'''A Graphviz table.

    ::

        >>> table = documentationtools.GraphvizTable(
        ...     attributes={'style': 'rounded'},
        ...     )
        >>> row_1 = documentationtools.GraphvizTableRow()
        >>> row_1.append(documentationtools.GraphvizTableCell(label='foo'))
        >>> row_1.append(documentationtools.GraphvizTableVerticalRule())
        >>> row_1.append(documentationtools.GraphvizTableCell(label='bar'))
        >>> row_2 = documentationtools.GraphvizTableRow()
        >>> row_2.append(documentationtools.GraphvizTableCell(label='quux'))
        >>> table.extend([row_1, row_2])
        >>> print(table)
        <
        <TABLE STYLE="ROUNDED">
            <TR>
                <TD>foo</TD>
                <VR/>
                <TD>bar</TD>
            </TR>
            <TR>
                <TD>quux</TD>
            </TR>
        </TABLE>>

    ::

        >>> node = documentationtools.GraphvizNode()
        >>> node.append(table)
        >>> print(node)
        node_0 [label=<
            <TABLE STYLE="ROUNDED">
                <TR>
                    <TD>foo</TD>
                    <VR/>
                    <TD>bar</TD>
                </TR>
                <TR>
                    <TD>quux</TD>
                </TR>
            </TABLE>>];

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Graphviz'

    __slots__ = (
        '_attributes',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        children=None,
        name=None,
        attributes=None,
        ):
        TreeContainer.__init__(
            self,
            children=children,
            name=name,
            )
        if attributes is not None:
            attributes = dict(attributes)
        self._attributes = attributes

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Get string representation of Graphviz table.

        Returns string.
        '''
        result = ['<']
        attribute_string = self._attribute_string
        if attribute_string:
            result.append('<TABLE {}>'.format(attribute_string))
        else:
            result.append('<TABLE>')
        for x in self:
            for line in str(x).splitlines():
                result.append('    ' + line)
        result.append('</TABLE>>')
        result = '\n'.join(result)
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

    @property
    def _node_class(self):
        from abjad.tools import documentationtools
        prototype = (
            documentationtools.GraphvizTableRow,
            documentationtools.GraphvizTableHorizontalRule,
            )
        return prototype

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        r'''Gets Graphviz table attribute dictionary.

        Returns dictionary.
        '''
        return self._attributes
