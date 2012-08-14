from abjad.tools.abctools import AbjadObject


class ContainmentSignature(AbjadObject):
    r'''.. versionadded:: 2.9

    Containment signature of Abjad component::

        >>> score = Score(r"""\context Staff = "CustomStaff" { """
        ...     r"""\context Voice = "CustomVoice" { c' d' e' f' } }""")
        >>> score.name = 'CustomScore'

    ::

        >>> f(score)
        \context Score = "CustomScore" <<
            \context Staff = "CustomStaff" {
                \context Voice = "CustomVoice" {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            }
        >>

    ::

        >>> componenttools.component_to_containment_signature(score.leaves[0])
        ContainmentSignature(Note-..., Voice-'CustomVoice', Staff-..., Score-'CustomScore')

    Returned only by componenttools.component_to_containment_signature().

    Used for thread iteration behind the scenes.
    '''

    ### INITIALIZER ###

    def __init__(self):
        self._root = None
        self._root_str = ''
        self._self = None
        self._score = None
        self._staff = None
        self._staff_group = None
        self._voice = None

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        return isinstance(arg, ContainmentSignature) and \
            self._voice == arg._voice and \
            self._staff == arg._staff and \
            self._staff_group == arg._staff_group and \
            self._score == arg._score and \
            self._root == arg._root

    def __ne__(self, arg):
        return not self == arg

    def __repr__(self):
        values = [x[-1] for x in self._parts]
        values = ', '.join(values)
        return '{}({})'.format(self._class_name, values)

    def __str__(self):
        result = []
        for name, value in reversed(self._parts):
            result.append('%10s: %s' % (name, value))
        return '\n'.join(result)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _parts(self):
        result = []
        attrs = ('self', 'voice', 'staff', 'staff_group', 'score')
        for attr in attrs:
            if getattr(self, '_' + attr, None) is not None:
                result.append((attr, getattr(self, '_' + attr)))
        return result
