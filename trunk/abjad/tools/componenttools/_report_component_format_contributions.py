from abjad.tools.componenttools.Component import Component


def _report_component_format_contributions(component, verbose=False, output='screen'):
    r'''Read-only string report of all format-time contributions
    made to `component` by all the different parts of the Abjad
    system plumbing.

    Set `verbose` to True or False.

    Set `output` to 'screen' or 'string'.
    '''
    from abjad.tools.spannertools import Spanner
    from abjad.tools.leaftools.Leaf import Leaf

    if isinstance(component, Leaf):
        return component._report_format_contributors()
    if isinstance(component, Component):
        return component._formatter.report(verbose=verbose, output=output)
    elif isinstance(component, Spanner):
        return component._format.report(output=output)
    else:
        raise TypeError('neither component nor spanner: "%s".' % component)
