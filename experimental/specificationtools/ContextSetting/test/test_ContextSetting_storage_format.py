from experimental import specificationtools


def test_ContextSetting_storage_format_01():

    anchor = specificationtools.ScoreObjectIndicator(segment='1')
    start = specificationtools.Timepoint(anchor=anchor)
    stop = specificationtools.Timepoint(anchor=anchor, edge=Right)
    timespan = specificationtools.Timespan(start=start, stop=stop)
    target = specificationtools.ContextSelection('Voice 1', timespan=timespan)
    setting = specificationtools.ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    r'''
    specificationtools.ContextSetting(
        specificationtools.ContextSelection(
            'Voice 1',
            timespan=specificationtools.Timespan(
                start=specificationtools.Timepoint(
                    anchor=specificationtools.ScoreObjectIndicator(
                        segment='1'
                        )
                    ),
                stop=specificationtools.Timepoint(
                    anchor=specificationtools.ScoreObjectIndicator(
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

    setting.storage_format == "specificationtools.ContextSetting(\n\tspecificationtools.ContextSelection(\n\t\t'Voice 1',\n\t\ttimespan=specificationtools.Timespan(\n\t\t\tstart=specificationtools.Timepoint(\n\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\tsegment='1'\n\t\t\t\t\t)\n\t\t\t\t),\n\t\t\tstop=specificationtools.Timepoint(\n\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\tsegment='1'\n\t\t\t\t\t),\n\t\t\t\tedge=Right\n\t\t\t\t)\n\t\t\t)\n\t\t),\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tpersistent=True,\n\ttruncate=False,\n\tfresh=False\n\t)"
