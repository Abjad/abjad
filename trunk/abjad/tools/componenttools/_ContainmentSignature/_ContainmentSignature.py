from abjad.core import _StrictComparator


class _ContainmentSignature(_StrictComparator):

    def __init__(self):
        self._root = None
        self._root_str = ''
        self._self = None
        self._score = None
        self._staff = None
        self._staffgroup = None
        self._voice = None

    ### OVERLOADS ###

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
        str = self.__str__()
        return '<' + ' * '.join(str.split('\n')) + ' >'

    def __str__(self):
        result = []
        result.append('        root: %s (%s)' % (self._root_str, self._root))
        result.append('     score: %s' % (self._score or ''))
        result.append('staffgroup: %s' % (self._staffgroup or ''))
        result.append('     staff: %s' % (self._staff or ''))
        result.append('     voice: %s' % (self._voice or ''))
        result.append('        self: %s' % self._self)
        return '\n'.join(result)
