# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools.documentationtools.ReSTDirective import ReSTDirective


class ReSTAutosummaryDirective(ReSTDirective):
    r'''A ReST Autosummary directive.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> toc = abjad.documentationtools.ReSTAutosummaryDirective()
            >>> for item in ['foo.Foo', 'bar.Bar', 'baz.Baz']:
            ...     toc.append(abjad.documentationtools.ReSTAutosummaryItem(text=item))
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
                    ),
                directive='autosummary'
                )

        ::

            >>> print(toc.rest_format)
            .. autosummary::
            <BLANKLINE>
            foo.Foo
            bar.Bar
            baz.Baz

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __setitem__(self, i, argument):
        r'''Sets item `i` to `argument`.

        Returns none.
        '''
        from abjad.tools import documentationtools
        newexpr = []
        for x in argument:
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
        r'''Directive of ReST autosummary diretive.

        Returns ``'autosummary'``.
        '''
        return 'autosummary'

    @property
    def node_class(self):
        r'''Node class of ReST autosummary directive.
        '''
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTAutosummaryItem,
            )
