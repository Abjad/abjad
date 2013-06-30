from abjad.tools.datastructuretools.TreeNode import TreeNode


class ReSTHorizontalRule(TreeNode):
    '''An ReST horizontal rule:

    ::

        >>> rule = documentationtools.ReSTHorizontalRule()
        >>> rule
        ReSTHorizontalRule()

    ::

        >>> print rule.rest_format
        --------

    Return `ReSTHorizontalRule` instance.
    '''

    ### PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        return ['--------']

    ### PUBLIC PROPERTIES ###

    @property
    def rest_format(self):
        return '\n'.join(self._rest_format_contributions)
