from abjad import Duration
from abjad.tools.mathtools import greatest_power_of_two_less_equal
from abjad.tools.notetools import make_notes
from abjad.tools.resttools import make_rests
from abjad.tools.tuplettools import FixedDurationTuplet
from abjad.tools.tuplettools import fix_contents_of_tuplets_in_expr
from abjad.tools.tuplettools import remove_trivial_tuplets_in_expr


class _RTMNode(object):

    def __init__(self, pulses_consumed, children):
        assert 0 < pulses_consumed
        self._pulses_consumed = int(pulses_consumed)
        self._children = tuple(children)

    def __call__(self, duration=Duration(1, 4)):

        def recurse(node, duration):
            tuplet = FixedDurationTuplet(duration, [])
            denominator =  greatest_power_of_two_less_equal((duration / node.width).denominator)
            for x in node:
                if isinstance(x, int):
                    if 0 < x:
                        tuplet.extend(make_notes(0, (x, denominator)))
                    else:
                        tuplet.extend(make_rests((abs(x), denominator)))
                else:
                    tuplet.append(recurse(x, Duration(x.pulses_consumed, denominator)))
            return tuplet

        result = recurse(self, duration * self._pulses_consumed)
        remove_trivial_tuplets_in_expr(result)
        return result

    def __iter__(self):
        for x in self.children:
            yield x

    def __repr__(self):
        return '(%d (%s))' % (self.pulses_consumed, ' '.join([repr(x) for x in self.children]))

    ### PUBLIC ATTRIBUTES ###

    @property
    def children(self):
        return self._children

    @property
    def pulses_consumed(self):
        return self._pulses_consumed

    @property
    def width(self):
        total = 0
        for x in self:
            if isinstance(x, int):
                total += abs(x)
            else:
                total += x.pulses_consumed
        return total
