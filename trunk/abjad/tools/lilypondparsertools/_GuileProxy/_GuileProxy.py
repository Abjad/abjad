from abjad import *
from abjad.tools.contexttools._Context import _Context


class _GuileProxy(object):

    def __init__(self, client):
        self.client = client

    ### OVERRIDES ###

    def __call__(self, function_name, args):
        if hasattr(self, function_name[1:]):
            result = getattr(self, function_name[1:])(*args)
            # print result
            return result
        raise Exception("LilyPondParser can't emulate music function %s." % function_name)

    ### FUNCTION EMULATORS ###

    def times(self, fraction, music):
        if not isinstance(music, _Context):
            return tuplettools.Tuplet(fraction, music[:])
        return tuplettools.Tuplet(fraction, [music])
