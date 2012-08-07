from abjad.tools import abctools
from abjad.tools import contexttools
from abjad.tools import mathtools
from abjad.tools import rhythmtreetools


class BeatHierarchy(abctools.AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_root_node', '_time_signature')

    ### INITIALIZER ###

    def __init__(self, time_signature):

        time_signature = contexttools.TimeSignatureMark(time_signature)
        self._time_signature = time_signature

        numerator, denominator = time_signature.numerator, time_signature.denominator
        factors = mathtools.factors(numerator)[1:]
        root = rhythmtreetools.RhythmTreeContainer(numerator)
        
        def recurse(node, factors):
            if factors:
                factor, factors = factors[0], factors[1:]
                duration = node.duration / factor

                if factor in (2, 3):
                    if factors:
                        for _ in range(factor):
                            child = rhythmtreetools.RhythmTreeContainer(duration)
                            node.append(child)
                            recurse(child, factors)
                    else:
                        for _ in range(factor):
                            node.append(rhythmtreetools.RhythmTreeLeaf())

                else:
                    parts = [3]
                    total = 3
                    while total < factor:
                        parts.append(2)
                        total += 2
                    for part in parts:
                        grouping = rhythmtreetools.RhythmTreeContainer(part * duration)
                        if factors:
                            for _ in range(part):
                                child = rhythmtreetools.RhythmTreeContainer(duration)
                                grouping.append(child)
                                recurse(child, factors)
                        else:
                            for _ in range(part):
                                grouping.append(rhythmtreetools.RhythmTreeLeaf())
                        node.append(grouping)

            else:
                node.extend([rhythmtreetools.RhythmTreeLeaf() for _ in range(node.duration)])

        recurse(root, factors)
        self._root_node = root

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def root_node(self):
        return self._root_node

    @property
    def rtm_format(self):
        return self._root_node.rtm_format

    @property
    def time_signature(self):
        return self._time_signature
