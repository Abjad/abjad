def _require(*types):
    r'''.. versionadded:: 2.6

    NOTE: this code is experimental in Abjad 2.6 and should not yet
    be applied to functions in the public API.

    Work remains to be done to investigate Sphinx's
    interactions with this type of decorator.

    Return a decorator function that requires specified types.

    Example to require a string then a numeric argument:
    ``@require(str, (int, long, float))`` prior to function definition.

    Taken from ActiveState.
    '''
    def deco(func):
        '''
        Decorator function to be returned from require().  Returns a function
        wrapper that validates argument types.
        '''
        def wrapper (*args):
            '''
            Function wrapper that checks argument types.
            '''
            assert len(args) == len(types), 'Wrong number of arguments.'
            for a, t in zip(args, types):
                if type(t) == type(()):
                    # any of these types are ok
                    assert sum(isinstance(a, tp) for tp in t) > 0, '''\
                        %s is not a valid type.  Valid types:
                        %s
                        ''' % (a, '\n'.join(str(x) for x in t))
                assert isinstance(a, t), '%s is not a %s type' % (a, t)
            return func(*args)
        return wrapper
    return deco
