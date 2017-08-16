from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTHorizontalRule(TreeNode):
    r'''A ReST horizontal rule.

    ..  container:: example

        ::

            >>> rule = abjad.documentationtools.ReSTHorizontalRule()
            >>> rule
            ReSTHorizontalRule()

        ::

            >>> print(rule.rest_format)
            --------

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    __slots__ = ()

    ### PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        return ['--------']

    ### PUBLIC PROPERTIES ###

    @property
    def rest_format(self):
        r'''ReST format of ReSt horizontal rule.

        Returns text.
        '''
        return '\n'.join(self._rest_format_contributions)
