def _invert_quality_indicator(intervals, inversion):
    from abjad.tools import seqtools
    if isinstance(inversion, int):
        #self.rotate(-inversion)
        intervals = seqtools.rotate_sequence(intervals, -inversion)
        rotation = -inversion
    elif inversion == 'root':
        rotation = 0
    elif inversion == 'first':
        #self.rotate(-1)
        intervals = seqtools.rotate_sequence(intervals, -1)
        rotation = -1
    elif inversion == 'second':
        #self.rotate(-2)
        intervals = seqtools.rotate_sequence(intervals, -2)
        rotation = -2
    elif inversion == 'third':
        #self.rotate(-3)
        intervals = seqtools.rotate_sequence(intervals, -3)
        rotation = -3
    elif inversion == 'fourth':
        #self.rotate(-4)
        intervals = seqtools.rotate_sequence(intervals, -4)
        rotation = -4
    else:
        raise ValueError('unknown inversion indicator: %s' % inversion)
    return intervals, rotation
