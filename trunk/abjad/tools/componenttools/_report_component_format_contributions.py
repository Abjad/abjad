from abjad.tools.componenttools._Component import _Component


def _report_component_format_contributions(component, verbose=False, output='screen'):
    r'''Read-only string report of all format-time contributions
    made to `component` by all the different parts of the Abjad
    system plumbing.

    Set `verbose` to True or False.

    Set `output` to 'screen' or 'string'.
    '''
    from abjad.tools.spannertools import Spanner
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools.leaftools._format_leaf import _report_leaf_format_contributors

    if isinstance(component, _Leaf):
        return _report_leaf_format_contributors(component)
    if isinstance(component, _Component):
        return component._formatter.report(verbose = verbose, output = output)
    elif isinstance(component, Spanner):
        return component._format.report(output = output)
    else:
        raise TypeError('neither component nor spanner: "%s".' % component)
