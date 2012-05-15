def report_spanner_format_contributions(spanner, screen=True):
    r'''.. versionadded:: 2.9

    Report spanner format contributions for every leaf to which spanner attaches.

        abjad> staff = Staff("c8 d e f")
        abjad> spanner = spannertools.BeamSpanner(staff[:])

    ::

        abjad> formattools.report_spanner_format_contributions(spanner)
        c8  before: []
             after: []
              left: []
             right: ['[']

        d8  before: []
             after: []
              left: []
             right: []

        e8  before: []
             after: []
              left: []
             right: []

        f8  before: []
             after: []
              left: []
             right: [']']

    Return none or return string.
    '''
    result = ''
    for leaf in spanner.leaves:
        result += str(leaf)
        result += '\tbefore: %s\n' % spanner._format._before(leaf)
        result += '\t after: %s\n' % spanner._format._after(leaf)
        result += '\t  left: %s\n' % spanner._format._left(leaf)
        result += '\t right: %s\n' % spanner._format._right(leaf)
        result += '\n'
    if result[-1] == '\n':
        result = result[:-1]
    if screen:
        print result
    else:
        return result
