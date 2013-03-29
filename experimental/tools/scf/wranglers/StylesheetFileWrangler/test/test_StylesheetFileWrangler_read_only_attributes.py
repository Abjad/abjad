import scf


def test_StylesheetFileWrangler_read_only_attributes_01():

    studio = scf.studio.Studio()
    wrangler = studio.stylesheet_file_wrangler

    assert '/Users/trevorbaca/Documents/baca/scf/stylesheets/clean_letter_14.ly' in \
        wrangler.list_score_external_asset_path_names()
