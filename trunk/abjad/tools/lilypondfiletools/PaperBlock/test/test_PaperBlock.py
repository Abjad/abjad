from abjad import *


def test_PaperBlock_01():

    pb = lilypondfiletools.PaperBlock()
    pb.top_margin = 15
    pb.left_margin = 15
    pb.markup_system_spacing__basic_distance = 8

    r'''
    \paper {
        left-margin = #15
        markup-system-spacing #'basic-distance = #8
        top-margin = #15
    }
    '''
    assert pb.format == "\\paper {\n\tleft-margin = #15\n\tmarkup-system-spacing #'basic-distance = #8\n\ttop-margin = #15\n}"
