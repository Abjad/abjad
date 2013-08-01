# -*- encoding: utf-8 -*-
def report_spanner_format_contributions(spanner):
    r'''Report spanner format contributions for every leaf 
    to which spanner attaches:

        >>> staff = Staff("c8 d e f")
        >>> spanner = spannertools.BeamSpanner(staff[:])

    ::

        >>> print formattools.report_spanner_format_contributions(spanner)
        c8  before: []
             after: []
             right: ['[']
        <BLANKLINE>
        d8  before: []
             after: []
             right: []
        <BLANKLINE>
        e8  before: []
             after: []
             right: []
        <BLANKLINE>
        f8  before: []
             after: []
             right: [']']

    Return none or return string.
    '''
    result = ''
    for leaf in spanner.leaves:
        result += str(leaf)
        result += '\tbefore: %s\n' % spanner._format_before_leaf(leaf)
        result += '\t after: %s\n' % spanner._format_after_leaf(leaf)
        result += '\t right: %s\n' % spanner._format_right_of_leaf(leaf)
        result += '\n'
    if result[-1] == '\n':
        result = result[:-1]
    return result
