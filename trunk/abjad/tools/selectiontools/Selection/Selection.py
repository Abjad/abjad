import types


class Selection(object):
    '''Selection of components taken from a single score.

    Selections will eventually model all user selections.

    This means that selections will eventually serve as input
    to and output from most functions in the API.

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_music',
        )

    _default_positional_input_arguments = (
        [],
        )

    ### INITIALIZER ###

    def __init__(self, music=None):
        if music is None:
            music = ()
        elif isinstance(music, (tuple, list)):
            music = tuple(music)
        elif isinstance(music, Selection):
            music = tuple(music)
        elif isinstance(music, types.GeneratorType):
            music = tuple(music)
        else:
            music = (music, )
        self._music = tuple(music)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        '''Cocatenate `expr` to selection.

        Return new selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = self._music + expr._music
            return type(self)(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = self._music + tuple(expr)
        return type(self)(music)

    def __contains__(self, expr):
        '''True when `expr` is in selection. Otherwise false.

        Return boolean.
        '''
        return expr in self._music

    def __eq__(self, expr):
        '''True when selection and `expr` are of the same type
        and when music of selection equals music of `expr`.
        Otherwise false.

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            return self._music == expr._music
        # eventually remove this permissive branch
        # and force the use of selections only
        elif isinstance(expr, (list, tuple)):
            return self._music == tuple(expr)

    def __getitem__(self, expr):
        '''Get item `expr` from selection.

        Return component from selection.
        '''
        result = self._music.__getitem__(expr)
        if isinstance(result, tuple):
            selection = type(self)()
            selection._music = result[:]
            result = selection
        return result

    def __len__(self):
        '''Number of components in selection.

        Return nonnegative integer.
        '''
        return len(self._music)

    def __ne__(self, expr):
        return not self == expr

    def __radd__(self, expr):
        '''Concatenate selection to `expr`.

        Return newly created selection.
        '''
        assert isinstance(expr, (type(self), list, tuple))
        if isinstance(expr, type(self)):
            music = expr._music + self._music
            #return SequentialSelection(music)
            return Selection(music)
        # eventually remove this permissive branch 
        # and force the use of selections only
        elif isinstance(expr, (tuple, list)):
            music = tuple(expr) + self._music
        #return SequentialSelection(music)
        return Selection(music)

    def __repr__(self):
        '''Representation of selection in Python interpreter.

        Return string.
        '''
        return '{}{!r}'.format(self.__class__.__name__, self._music)

    ### PRIVATE METHODS ###

    def _get_marks(self, mark_classes=None, recurse=True):
        result = []
        for component in self._iterate_components(recurse=recurse):
            marks = component.get_marks(mark_classes=mark_classes)
            result.extend(marks)
        return tuple(result)

    def _iterate_components(self, recurse=True, reverse=False):
        from abjad.tools import iterationtools
        if recurse:
            return iterationtools.iterate_components_in_expr(self)
        else:
            return self._iterate_top_level_components(reverse=reverse)

    def _iterate_top_level_components(self, reverse=False):
        if reverse:
            for component in reversed(self):
                yield component
        else:
            for component in self:
                yield component
