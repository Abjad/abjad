# -*- encoding: utf-8 -*-
r'''Source: PythonDecorateLibrary:
See: https://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
'''
#import collections
#import functools
#from abjad.tools.abctools.AbjadObject import AbjadObject
#
#
#class Memoize(AbjadObject):
#    r'''Memoize decorator.
#
#    Caches a function's return value.
#    '''
#
#    ### INITIALIZER ###
#
#    def __init__(self, function=None):
#       self.function = function
#       self.cache = {}
#
#    ### SPECIAL METHODS ###
#
#    def __call__(self, *args):
#        r'''Calls decorator on `args`.
#
#        Returns cached value.
#        '''
#        if not isinstance(args, collections.Hashable):
#            # mutable objects can not cache;
#            # reevaluates function instead of blowing up
#            return self.function(*args)
#        if args in self.cache:
#            return self.cache[args]
#        else:
#            value = self.function(*args)
#            self.cache[args] = value
#            return value
#
#    def __get__(self, obj, objtype):
#        r'''Supports instance methods.
#        '''
#        return functools.partial(self.__call__, obj)


class Memoize(dict):
    r'''Memoize decorator.

    Caches function return value.
    '''

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
