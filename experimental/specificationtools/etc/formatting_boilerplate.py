# use this in temporary test files while working on specificationtools tests

lilypond_file = lilypondfiletools.make_floating_time_signature_lilypond_file(score)
lilypond_file.header_block.title = markuptools.make_centered_title_markup('Quartetto', font_size=12)
lilypond_file.score.set.proportionalNotationDuration = schemetools.SchemeMoment((1, 48))
show(lilypond_file)
