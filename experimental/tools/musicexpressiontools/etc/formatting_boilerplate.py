# -*- encoding: utf-8 -*-
# use this in temporary test files while working on musicexpressiontools tests

lilypond_file = lilypondfiletools.make_floating_time_signature_lilypond_file(score)
testtools.apply_additional_layout(lilypond_file)
lilypond_file.header_block.title = markuptools.make_centered_title_markup('Étude', font_size=6)
contextualize(lilypond_file.score).proportionalNotationDuration = schemetools.SchemeMoment((1, 48))
show(lilypond_file)


# use this in committed test files while working on musicexpressiontools tests

    current_function_name = testtools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert format(score) == testtools.read_test_output(__file__, current_function_name)
