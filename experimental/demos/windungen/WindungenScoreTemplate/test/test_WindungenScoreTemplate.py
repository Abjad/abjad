from experimental.demos.windungen.WindungenScoreTemplate import WindungenScoreTemplate



def test_WindungenScoreTemplate_01():
    score_template = WindungenScoreTemplate()
    score = score_template()
    result = score.lilypond_format
