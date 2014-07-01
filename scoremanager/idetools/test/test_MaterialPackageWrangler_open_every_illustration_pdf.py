# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_open_every_illustration_pdf_01():

    package_names = ('pitch_range_inventory', 'tempo_inventory')
    paths = []
    for name in package_names:
        path = os.path.join(
            ide._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            name,
            'illustration.pdf',
            )
        paths.append(path)

    input_ = 'red~example~score m io* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents
    assert ide._session._attempted_to_open_file
    assert 'Will open ...' in contents
    for path in paths:
        assert path in contents