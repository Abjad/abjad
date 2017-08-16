from abjad.tools.datastructuretools import TreeContainer


class GraphvizTable(TreeContainer):
    r'''A Graphviz table.

    ..  container:: example

        ::

            >>> table = abjad.graphtools.GraphvizTable(
            ...     attributes={'style': 'rounded'},
            ...     )
            >>> row_1 = abjad.graphtools.GraphvizTableRow()
            >>> row_1.append(abjad.graphtools.GraphvizTableCell(label='foo'))
            >>> row_1.append(abjad.graphtools.GraphvizTableVerticalRule())
            >>> row_1.append(abjad.graphtools.GraphvizTableCell(label='bar'))
            >>> row_2 = abjad.graphtools.GraphvizTableRow()
            >>> row_2.append(abjad.graphtools.GraphvizTableCell(label='quux'))
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

            >>> node = abjad.graphtools.GraphvizNode()
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
        from abjad.tools import graphtools
        prototype = (
            graphtools.GraphvizTableRow,
            graphtools.GraphvizTableHorizontalRule,
            )
        return prototype

    ### PUBLIC PROPERTIES ###

    @property
    def attributes(self):
        r'''Gets Graphviz table attribute dictionary.

        Returns dictionary.
        '''
        return self._attributes
