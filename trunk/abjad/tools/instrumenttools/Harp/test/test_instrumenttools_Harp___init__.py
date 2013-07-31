# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Harp___init___01():

    harp = instrumenttools.Harp()

    assert isinstance(harp, instrumenttools.Harp)
