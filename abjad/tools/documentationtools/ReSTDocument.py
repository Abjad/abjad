# -*- coding: utf-8 -*-
from abjad.tools.datastructuretools.TreeContainer import TreeContainer


class ReSTDocument(TreeContainer):
    r'''A ReST document tree.

    ::

        >>> document = documentationtools.ReSTDocument()
        >>> document
        ReSTDocument()

    ::

        >>> document.append(documentationtools.ReSTHeading(
        ...     level=0, text='Hello World!'))
        >>> document.append(documentationtools.ReSTParagraph(
        ...     text='blah blah blah'))
        >>> toc = documentationtools.ReSTTOCDirective()
        >>> toc.append('foo/bar')
        >>> toc.append('bar/baz')
        >>> toc.append('quux')
        >>> document.append(toc)

    ::

        >>> document
        ReSTDocument(
            children=(
                ReSTHeading(
                    level=0,
                    text='Hello World!'
                    ),
                ReSTParagraph(
                    text='blah blah blah',
                    wrap=True
                    ),
                ReSTTOCDirective(
                    children=(
                        ReSTTOCItem(
                            text='foo/bar'
                            ),
                        ReSTTOCItem(
                            text='bar/baz'
                            ),
                        ReSTTOCItem(
                            text='quux'
                            ),
                        ),
                    directive='toctree'
                    ),
                )
            )

    ::

        >>> print(document.rest_format)
        ############
        Hello World!
        ############
        <BLANKLINE>
        blah blah blah
        <BLANKLINE>
        .. toctree::
        <BLANKLINE>
           foo/bar
           bar/baz
           quux

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    ### PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        result = []
        for child in self.children:
            result.extend(child._rest_format_contributions)
            result.append('')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def node_class(self):
        r'''Node class of ReST document.
        '''
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTDirective,
            documentationtools.ReSTHeading,
            documentationtools.ReSTHorizontalRule,
            documentationtools.ReSTParagraph,
            )

    @property
    def rest_format(self):
        r'''ReST format of ReST document.
        '''
        return '\n'.join(self._rest_format_contributions)
