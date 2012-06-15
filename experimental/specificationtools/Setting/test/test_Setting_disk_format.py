from experimental import specificationtools


def test_Setting_disk_format_01():

    anchor = specificationtools.ScoreObjectIndicator(segment='1')
    start = specificationtools.TemporalCursor(anchor=anchor)
    stop = specificationtools.TemporalCursor(anchor=anchor, edge=Right)
    scope = specificationtools.TemporalScope(start=start, stop=stop)
    target = specificationtools.ContextSelection('Voice 1', scope=scope)
    setting = specificationtools.Setting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    r'''
    specificationtools.Setting(
        specificationtools.ContextSelection(
            'Voice 1',
            scope=specificationtools.TemporalScope(
                start=specificationtools.TemporalCursor(
                    anchor=specificationtools.ScoreObjectIndicator(
                        segment='1'
                        )
                    ),
                stop=specificationtools.TemporalCursor(
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

    setting._disk_format == "specificationtools.Setting(\n\tspecificationtools.ContextSelection(\n\t\t'Voice 1',\n\t\tscope=specificationtools.TemporalScope(\n\t\t\tstart=specificationtools.TemporalCursor(\n\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\tsegment='1'\n\t\t\t\t\t)\n\t\t\t\t),\n\t\t\tstop=specificationtools.TemporalCursor(\n\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\tsegment='1'\n\t\t\t\t\t),\n\t\t\t\tedge=Right\n\t\t\t\t)\n\t\t\t)\n\t\t),\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tpersistent=True,\n\ttruncate=False,\n\tfresh=False\n\t)"
