# -*- coding: utf-8 -*-


def example_function(expr):
    r'''This is a multiline docstring.

    This is the third line of the docstring.
    '''
    # This is a comment.
    print('Entering example function.')
    try:
        expr = expr + 1
    except TypeError:
        print('Wrong type!')
    print(expr)
    print('Leaving example function.')
