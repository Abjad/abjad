from abjad.tools.datastructuretools.TreeContainer import TreeContainer


class ReSTDocument(TreeContainer):
    '''An ReST document tree:

    ::

        >>> document = documentationtools.ReSTDocument()
        >>> document
        ReSTDocument()

    ::

        >>> document.append(documentationtools.ReSTHeading(level=0, text='Hello World!'))
        >>> document.append(documentationtools.ReSTParagraph(text='blah blah blah'))
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
                            )
                        )
                    )
                )
            )

    ::

        >>> print document.rest_format
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

    Return `ReSTDocument` instance.
    '''

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        result = []
        for child in self.children:
            result.extend(child._rest_format_contributions)
            result.append('')
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def node_klass(self):
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTDirective,
            documentationtools.ReSTHeading,
            documentationtools.ReSTHorizontalRule,
            documentationtools.ReSTParagraph,
            )

    @property
    def rest_format(self):
        return '\n'.join(self._rest_format_contributions)

