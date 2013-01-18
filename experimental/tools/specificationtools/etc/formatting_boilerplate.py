# use this in temporary test files while working on specificationtools tests

lilypond_file = lilypondfiletools.make_floating_time_signature_lilypond_file(score)
lilypond_file.header_block.title = markuptools.make_centered_title_markup('Étude', font_size=6)
lilypond_file.score.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 48))
show(lilypond_file)


# use this in committed test files while working on specificationtools tests

current_function_name = introspectiontools.get_current_function_name()
testtools.write_test_output(score, __file__, current_function_name)
assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
