from abjad import *


def test_instrumenttools_UntunedPercussion___init___01():

    percussion = instrumenttools.UntunedPercussion()

    assert isinstance(percussion, instrumenttools.UntunedPercussion)
