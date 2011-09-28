from abjad.tools.componenttools._report_component_format_contributions import _report_component_format_contributions


def report_component_format_contributions_as_string(component, verbose=False):
    r'''.. versionadded:: 1.1

    Report `component` format contributions as string.

    Set `verbose` to True or False.
    '''

    return _report_component_format_contributions(component, verbose=verbose, output='string')
