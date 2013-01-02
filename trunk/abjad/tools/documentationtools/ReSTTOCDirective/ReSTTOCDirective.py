from abjad.tools import datastructuretools
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTTOCDirective(ReSTDirective):
    '''An ReST TOCTree directive:

    ::

        >>> toc = documentationtools.ReSTTOCDirective()
        >>> for item in ['foo/index', 'bar/index', 'baz/index']:
        ...     toc.append(documentationtools.ReSTTOCItem(text=item))
        ...
        >>> toc.options['maxdepth'] = 1
        >>> toc.options['hidden'] = True
        >>> toc
        ReSTTOCDirective(
            children=(
                ReSTTOCItem(
                    text='foo/index'
                    ),
                ReSTTOCItem(
                    text='bar/index'
                    ),
                ReSTTOCItem(
                    text='baz/index'
                    )
                ),
            options={
                'hidden': True,
                'maxdepth': 1
                }
            )

    ::

        >>> print toc.rest_format
        .. toctree::
           :hidden:
           :maxdepth: 1
        <BLANKLINE>
           foo/index
           bar/index
           baz/index

    Return `ReSTTOCDirective` instance.
    '''

    ### SPECIAL METHODS ###

    def __setitem__(self, i, expr):
        from abjad.tools import documentationtools
        newexpr = []
        for x in expr:
            if isinstance(x, str):
                newexpr.append(documentationtools.ReSTTOCItem(text=x))
            else:
                newexpr.append(x)
        datastructuretools.TreeContainer.__setitem__(self, i, newexpr)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _children_rest_format_contributions(self):
        result = ['']
        for child in self.children:
            contribution = child._rest_format_contributions
            for x in contribution:
                if x:
                    result.append('   ' + x)
                else:
                    result.append(x)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directive(self):
        return 'toctree'

    @property
    def node_klass(self):
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTTOCItem,
            )
