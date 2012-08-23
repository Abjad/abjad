from abjad.tools.marktools.Mark import Mark


class BendAfter(Mark):
    r'''Abjad model of a fall or doit::

        >>> note = Note("c'4")

    ::

        >>> marktools.BendAfter(-4)(note)
        BendAfter(-4.0)(c'4)

    ::

        >>> f(note)
        c'4 - \bendAfter #'-4.0

    BendAfter implements ``__slots__``.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = (-4, )

    ### INITIALIZER ###

    def __init__(self, *args):
        Mark.__init__(self)
        self._format_slot = 'right'
        if len(args) == 1 and isinstance(args[0], type(self)):
            self.bend_amount = args[0].bend_amount
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            self.bend_amount = args[0]
        else:
            raise ValueError('can not initialize stem tremolo.')

    ## OVERRIDE ##

    def __copy__(self, *args):
        #return type(self)(self.bend_amount)
        new = type(self)(self.bend_amount)
        new.format_slot = self.format_slot
        return new

    __deepcopy__ = __copy__

    def __eq__(self, expr):
        assert isinstance(expr, type(self))
        if self.bend_amount == expr.bend_amount:
            return True
        return False

    def __str__(self):
        return r"- \bendAfter #'%s" % self.bend_amount

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return '%s' % self.bend_amount

    ### PUBLIC PROPERTIES ###

    @property
    def lilypond_format(self):
        r'''Read-only LilyPond format string::

            >>> bend = marktools.BendAfter(-4)
            >>> bend.lilypond_format
            "- \\bendAfter #'-4.0"

        Return string.
        '''
        return str(self)

    @apply
    def bend_amount():
        def fget(self):
            '''Get bend amount::

                >>> bend = marktools.BendAfter(8)
                >>> bend.bend_amount
                8.0

            Set bend amount::

                >>> bend.bend_amount = -4
                >>> bend.bend_amount
                -4.0

            Set float.
            '''
            return self._bend_amount
        def fset(self, bend_amount):
            assert isinstance(bend_amount, (int, float))
            self._bend_amount = float(bend_amount)
        return property(**locals())
