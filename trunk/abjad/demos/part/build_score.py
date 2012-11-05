def build_score():
    from abjad.demos import part

    score_template = part.PartCantusScoreTemplate()
    score = score_template()

    part.add_bell_music_to_score(score)
    part.add_string_music_to_score(score)
    part.apply_dynamic_marks(score)
    part.apply_expressive_marks(score)
    part.apply_page_breaks(score)

    return score
