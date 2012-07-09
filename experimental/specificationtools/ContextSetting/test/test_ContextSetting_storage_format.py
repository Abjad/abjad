from experimental import selectortools
from experimental import specificationtools
from experimental import timespantools


def test_ContextSetting_storage_format_01():

    anchor = selectortools.SegmentSelector(index='red')
    start = timespantools.Timepoint(anchor=anchor)
    stop = timespantools.Timepoint(anchor=anchor, edge=Right)
    timespan = timespantools.Timespan(start=start, stop=stop)
    target = selectortools.SingleContextSelection('Voice 1', timespan=timespan)
    setting = specificationtools.ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    r'''
    specificationtools.ContextSetting(
        selectortools.SingleContextSelection(
            'Voice 1',
            timespan=timespantools.Timespan(
                start=timespantools.Timepoint(
                    anchor=selectortools.CounttimeComponentSelector(
                        segment='1'
                        )
                    ),
                stop=timespantools.Timepoint(
                    anchor=selectortools.CounttimeComponentSelector(
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

    assert setting.storage_format == "specificationtools.ContextSetting(\n\tselectortools.SingleContextSelection(\n\t\t'Voice 1',\n\t\ttimespan=timespantools.Timespan(\n\t\t\tstart=timespantools.Timepoint(\n\t\t\t\tanchor=selectortools.SegmentSelector(\n\t\t\t\t\tindex='red'\n\t\t\t\t\t)\n\t\t\t\t),\n\t\t\tstop=timespantools.Timepoint(\n\t\t\t\tanchor=selectortools.SegmentSelector(\n\t\t\t\t\tindex='red'\n\t\t\t\t\t),\n\t\t\t\tedge=Right\n\t\t\t\t)\n\t\t\t)\n\t\t),\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tpersistent=True,\n\ttruncate=False,\n\tfresh=False\n\t)"
