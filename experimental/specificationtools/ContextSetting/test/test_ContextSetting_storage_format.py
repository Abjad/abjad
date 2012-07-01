from experimental import specificationtools
from experimental import timespantools


def test_ContextSetting_storage_format_01():

    anchor = specificationtools.ComponentSelector(segment='1')
    start = timespantools.Timepoint(anchor=anchor)
    stop = timespantools.Timepoint(anchor=anchor, edge=Right)
    timespan = timespantools.Timespan(start=start, stop=stop)
    target = specificationtools.ContextSelection('Voice 1', timespan=timespan)
    setting = specificationtools.ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    r'''
    specificationtools.ContextSetting(
        specificationtools.ContextSelection(
            'Voice 1',
            timespan=timespantools.Timespan(
                start=timespantools.Timepoint(
                    anchor=specificationtools.ComponentSelector(
                        segment='1'
                        )
                    ),
                stop=timespantools.Timepoint(
                    anchor=specificationtools.ComponentSelector(
                        segment='1'
                        ),
                    edge=Right
                    )
                )
            ),
        'time_signatures',
        [(4, 8), (3, 8)],
        persistent=True,
        truncate=True,
        fresh=False
        )
    '''

    setting.storage_format == "specificationtools.ContextSetting(\n\tspecificationtools.ContextSelection(\n\t\t'Voice 1',\n\t\ttimespan=timespantools.Timespan(\n\t\t\tstart=timespantools.Timepoint(\n\t\t\t\tanchor=specificationtools.ComponentSelector(\n\t\t\t\t\tsegment='1'\n\t\t\t\t\t)\n\t\t\t\t),\n\t\t\tstop=timespantools.Timepoint(\n\t\t\t\tanchor=specificationtools.ComponentSelector(\n\t\t\t\t\tsegment='1'\n\t\t\t\t\t),\n\t\t\t\tedge=Right\n\t\t\t\t)\n\t\t\t)\n\t\t),\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tpersistent=True,\n\ttruncate=False,\n\tfresh=False\n\t)"
