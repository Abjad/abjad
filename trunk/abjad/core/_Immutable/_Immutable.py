class _Immutable(object):
    '''.. versionadded:: 2.0

    Base from which immutable custom classes can inherit.

    .. todo:: write code to check all Abjad system objects with slots and
        make sure none has a dict defined and taking up memory in the namespace of the object.
    '''

    __slots__ = ()

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self)

    __deepcopy__ = __copy__

    def __delattr__(self, *args):
        raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)

    def __getstate__(self):
        return {}

    def __setattr__(self, *args):
        raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)

    def __setstate__(self, state):
        pass
