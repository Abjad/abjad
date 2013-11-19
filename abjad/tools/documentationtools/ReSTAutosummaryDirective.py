# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTAutosummaryDirective(ReSTDirective):
    r'''An ReST AutosummaryTree directive:

    ::

        >>> toc = documentationtools.ReSTAutosummaryDirective()
        >>> for item in ['foo.Foo', 'bar.Bar', 'baz.Baz']:
        ...     toc.append(documentationtools.ReSTAutosummaryItem(text=item))
        ...
        >>> toc
        ReSTAutosummaryDirective(
            children=(
                ReSTAutosummaryItem(
                    text='foo.Foo'
                    ),
                ReSTAutosummaryItem(
                    text='bar.Bar'
                    ),
                ReSTAutosummaryItem(
                    text='baz.Baz'
                    ),
                )
            )

    ::

        >>> print toc.rest_format
        .. autosummary::
        <BLANKLINE>
           foo.Foo
           bar.Bar
           baz.Baz

    Return `ReSTAutosummaryDirective` instance.
    '''

    ### SPECIAL METHODS ###

    def __setitem__(self, i, expr):
        from abjad.tools import documentationtools
        newexpr = []
        for x in expr:
            if isinstance(x, str):
                newexpr.append(documentationtools.ReSTAutosummaryItem(text=x))
            else:
                newexpr.append(x)
        datastructuretools.TreeContainer.__setitem__(self, i, newexpr)

    ### PRIVATE PROPERTIES ###

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

    ### PUBLIC PROPERTIES ###

    @property
    def directive(self):
        return 'autosummary'

    @property
    def node_class(self):
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTAutosummaryItem,
            )
