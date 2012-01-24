from abjad import *
from abjad.tools.contexttools._Context import _Context


class _GuileProxy(object):

    def __init__(self, client):
        self.client = client


    ### OVERRIDES ###


    def __call__(self, function_name, args):
        signature = self.client._current_module[function_name[1:]]['signature'][1:]
        print '_GuileProxy: %s, %s, %s' % (function_name, signature, args)
        if hasattr(self, function_name[1:]):
            result = getattr(self, function_name[1:])(*args)
            # print result
            return result
        raise Exception("LilyPondParser can't emulate music function %s." % function_name)


    ### FUNCTION EMULATORS ###


    def acciaccatura(self, music):
        grace = gracetools.Grace(music[:])
        grace.kind = 'acciaccatura'
        return grace


    # afterGrace


    def appoggiatura(self, music):
        grace = gracetools.Grace(music[:])
        grace.kind = 'appoggiatura'
        return grace


    def bar(self, string):
        return marktools.BarLine(string)


    def breathe(self):
        return marktools.LilyPondCommandMark('breathe', 'before')


    def clef(self, string):
        return contexttools.ClefMark(string)


    def grace(self, music):
        return gracetools.Grace(music[:])


    def key(self, notename_pitch, number_list):
        if number_list is None:
            number_list = 'major'
        return contexttools.KeySignatureMark(notename_pitch, number_list)


    def language(self, string):
        if string in self.client._language_pitch_names:
            self.client._parser_variables['language'] = string


    def makeClusters(self, music):
        return containertools.Cluster(music[:])


    def mark(self, label):
        if label is None:
            label = '\default'
        return marktools.LilyPondCommandMark('mark %s' % label)


    # pitchedTrill


    # relative


    def slashedGrace(self, music):
        grace = gracetools.Grace(music[:])
        grace.kind = 'slashedGrace'
        return grace


    def time(self, number_list, fraction):
        return contexttools.TimeSignatureMark(fraction)


    def times(self, fraction, music):
        if not isinstance(music, _Context):
            return tuplettools.Tuplet(fraction, music[:])
        return tuplettools.Tuplet(fraction, [music])


    # transpose


    # transposition


    # tweak

    
