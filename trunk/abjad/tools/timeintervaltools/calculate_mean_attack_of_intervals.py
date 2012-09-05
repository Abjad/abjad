from abjad.tools import durationtools



def calculate_mean_attack_of_intervals(intervals):
    '''Return Fraction of the average attack offset of `intervals`'''
    from abjad.tools import timeintervaltools

    tree = timeintervaltools.TimeIntervalTree(intervals)

    if not tree:
        return None

    return durationtools.Offset(sum([i.start for i in tree])) / len(tree)
