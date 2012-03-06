class _MutableAbjadObject(object):
    '''.. versionadded:: 2.8

    Base class to implement system-global functionality.

    _MutableAbjadObject and _ImmutableAbjadObject differ only in the implementation of __slots__.
    '''

    ### READ-ONLY ATTRIBUTES ###

    @property
    def class_name(self):
        return type(self).__name__ 
