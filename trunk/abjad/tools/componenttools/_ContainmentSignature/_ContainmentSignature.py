from abjad.tools.abctools import AbjadObject


class _ContainmentSignature(AbjadObject):

    def __init__(self):
        self._root = None
        self._root_str = ''
        self._self = None
        self._score = None
        self._staff = None
        self._staffgroup = None
        self._voice = None

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        return isinstance(arg, _ContainmentSignature) and \
            self._voice == arg._voice and \
            self._staff == arg._staff and \
            self._staffgroup == arg._staffgroup and \
            self._score == arg._score and \
            self._root == arg._root

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        string = self.__str__()
        return '<' + ' * '.join(string.split('\n')) + ' >'

    def __str__(self):
        result = []
        def helper(x):
            if x is None:
                return ''
            else:
                return x
        result.append('      root: %s (%s)' % (self._root_str, self._root))
        result.append('     score: %s' % helper(self._score))
        result.append('staffgroup: %s' % helper(self._staffgroup))
        result.append('     staff: %s' % helper(self._staff))
        result.append('     voice: %s' % helper(self._voice))
        result.append('      self: %s' % helper(self._self))
        return '\n'.join(result)
