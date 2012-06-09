from experimental.specificationtools.Setting import Setting


def test_Setting_disk_format_01():

    setting = Setting('1', 'Voice 1', None, 'time_signatures', [(4, 8), (3, 8)], True, True)

    r'''
    specification.Setting(
        '1',
        'Voice 1',
        None,
        'time_signatures',
        [(4, 8), (3, 8)],
        True,
        True,
        fresh=True
        )
    '''

    setting._disk_format == "specification.Setting(\n\t'1',\n\t'Voice 1',\n\tNone,\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tTrue,\n\tTrue,\n\tfresh=True\n\t)"
