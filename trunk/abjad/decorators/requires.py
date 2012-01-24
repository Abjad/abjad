import types


# TODO: figure out how to handle functions with **kwargs
def requires(*tests):
    r'''.. versionadded:: 2.6

    Function decorator to require input parameter `tests`.

    Example::

        abjad> from abjad.tools import mathtools
        abjad> from abjad.decorators import requires

    ::

        abjad> @requires(mathtools.is_nonnegative_integer, str)
        abjad> def multiply_string(n, string): return n * string

    ::

        abjad> multiply_string(2, 'bar')
        'barbar'

    ::

        abjad> multiply_string(2.5, 'bar')
        ...
        AssertionError: is_nonnegative_integer(2.5) does not return true.

    Decorator target is available like this::

        abjad> multiply_string.func_closure[1].cell_contents
        <function multiply_string at 0x104e512a8>

    Decorator tests are available like this::

        abjad> multiply_string.func_closure[0].cell_contents
        (<function is_nonnegative_integer at 0x104725d70>, <type 'str'>)
    
    Return decorated function in the form of function wrapper.
    '''
    def deco(func):
        '''
        Decorator function to be returned from requires().  
        Returns a function wrapper that validates arguments.
        '''
        def wrapper (*args):
            '''
            Function wrapper that validates arguments.
            '''
            assert len(args) == len(tests), 'wrong number of arguments.'
            for arg, test in zip(args, tests):
                if isinstance(test, tuple):
                    tuple_repr = [x.__name__ for x in test]
                    tuple_repr = ', '.join(tuple_repr)
                    tuple_repr = '({})'.format(tuple_repr)
                    error_message = 'isinstance({!r}, {}) does not return true.'.format(arg, tuple_repr)
                    assert isinstance(arg, test), error_message
                elif isinstance(test, types.TypeType):
                    error_message = 'isinstance({!r}, {}) does not return true.'.format(arg, test.__name__)
                    assert isinstance(arg, test), error_message
                else:
                    error_message = '{}({!r}) does not return true.'.format(test.__name__, arg)
                    assert test(arg), error_message
            return func(*args)
        # point Sphinx to correct docstring
        wrapper.__doc__ = func.__doc__
        return wrapper
    return deco
