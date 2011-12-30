from abjad.tools.contexttools.ContextMark import ContextMark


class ClefMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of a clef::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> contexttools.ClefMark('treble')(staff)
        ClefMark('treble')(Staff{4})

    ::

        abjad> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            d'8
            e'8
            f'8
        }

    Clef marks target the staff context by default.
    '''

    _format_slot = 'opening'
    #default_target_context = Staff

    def __init__(self, arg, target_context = None):
        from abjad.tools.stafftools.Staff import Staff
        ContextMark.__init__(self, target_context = target_context)
        if self.target_context is None:
            self._target_context = Staff
        if isinstance(arg, str):
            self._clef_name = arg
        elif isinstance(arg, type(self)):
            self._clef_name = arg.clef_name
        else:
            raise TypeError('can not init clef from %s.' % arg)

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self._clef_name, target_context = self.target_context)

    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self._clef_name == arg._clef_name
        return False

    ### PRIVATE ATTRIBUTES ###

    _clef_name_to_middle_c_position = { 'treble': -6, 'alto': 0, 'tenor': 2, 'bass': 6, }

    @property
    def _contents_repr_string(self):
        return repr(self._clef_name)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def clef_name():
        def fget(self):
            r'''Get clef name::

                abjad> clef = contexttools.ClefMark('treble')
                abjad> clef.clef_name
                'treble'

            Set clef name::

                abjad> clef.clef_name = 'alto'
                abjad> clef.clef_name
                'alto'

            Return string.
            '''
            return self._clef_name
        def fset(self, clef_name):
            assert isinstance(clef_name, str)
            self._clef_name = clef_name
        return property(**locals())

    @property
    def format(self):
        r'''Read-only LilyPond format of clef:

        ::

            abjad> clef = contexttools.ClefMark('treble')
            abjad> clef.format
            '\\clef "treble"'

        Return string.
        '''
        return r'\clef "%s"' % self._clef_name

    @property
    def middle_c_position(self):
        '''Read-only middle-C position of clef:

        ::

            abjad> clef = contexttools.ClefMark('treble')
            abjad> clef.middle_c_position
            -6

        Return integer number of stafflines.
        '''
        return self._clef_name_to_middle_c_position[self._clef_name]
