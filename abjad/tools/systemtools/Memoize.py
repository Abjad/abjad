# -*- coding: utf-8 -*-
r'''Source: PythonDecorateLibrary:
See: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
'''


class Memoize(dict):
    r'''Memoize decorator.

    Caches function return value.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Decorators'

    ### INITIALIZER ###

    def __init__(self, function=None):
        self.function = function

    ### SPECIAL METHODS ###

    def __call__(self, *args):
        r'''Calls decorator on `args`.

        Calls function on `args` and caches if no cached value is found.

        Returns cached value.
        '''
        return self[args]

    def __missing__(self, key):
        r'''Calls function on `*key` and caches.

        Returns cached value.
        '''
        result = self[key] = self.function(*key)
        return result
