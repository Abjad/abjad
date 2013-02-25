from abjad import *


def test_PaperBlock_01():

    paper_block = lilypondfiletools.PaperBlock()
    paper_block.top_margin = 15
    paper_block.left_margin = 15
    paper_block.markup_system_spacing__basic_distance = 8

    r'''
    \paper {
        left-margin = #15
        markup-system-spacing #'basic-distance = #8
        top-margin = #15
    }
    '''

    assert paper_block.lilypond_format == "\\paper {\n\tleft-margin = #15\n\tmarkup-system-spacing #'basic-distance = #8\n\ttop-margin = #15\n}"


def test_PaperBlock_02():
    '''Make sure scheme vectors format correctly.
    '''

    paper_block = lilypondfiletools.PaperBlock()
    paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)

    r'''
    \paper {
        system-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 12) (stretchability . 0))
    }
    '''

    assert paper_block.lilypond_format == "\\paper {\n\tsystem-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 12) (stretchability . 0))\n}"


def test_PaperBlock_03():

    paper_block = lilypondfiletools.PaperBlock()
    paper_block.append(schemetools.Scheme([
        'define', 'fonts', [
            'make-pango-font-tree',
            schemetools.Scheme('Baskerville', force_quotes=True),
            schemetools.Scheme('Baskerville', force_quotes=True),
            schemetools.Scheme('Baskerville', force_quotes=True),
            schemetools.Scheme(['/', 14, 20])
            ]
        ]))

    r'''
    \paper {
        #(define fonts (make-pango-font-tree "Baskerville" "Baskerville" "Baskerville" (/ 14 20)))
    }
    '''

    assert paper_block.lilypond_format == '\\paper {\n\t#(define fonts (make-pango-font-tree "Baskerville" "Baskerville" "Baskerville" (/ 14 20)))\n}'

