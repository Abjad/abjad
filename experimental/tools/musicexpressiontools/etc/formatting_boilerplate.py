# -*- encoding: utf-8 -*-
# use this in temporary test files while working on musicexpressiontools tests

maker = lilypondfiletools.make_floating_time_signature_lilypond_file
markup = markuptools.make_centered_title_markup('Étude', font_size=6)
moment = schemetools.SchemeMoment((1, 48))
lilypond_file = maker(score)
systemtools.TestManager.apply_additional_layout(lilypond_file)
lilypond_file.header_block.title = markup
set_(lilypond_file.score).proportionalNotationDuration = moment
show(lilypond_file)


# use this in committed test files while working on musicexpressiontools tests

    manager = systemtools.TestManager
    current_function_name = manager.get_current_function_name()
    manager.write_test_output(score, __file__, current_function_name)
    test_output == manager.read_test_output(__file__, current_function_name)
    assert format(score) == test_output
