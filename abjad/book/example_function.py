def example_function(argument):
    r'''This is a multiline docstring.

    This is the third line of the docstring.
    '''
    # This is a comment.
    print('Entering example function.')
    try:
        argument = argument + 1
    except TypeError:
        print('Wrong type!')
    print(argument)
    print('Leaving example function.')
