from abjad.tools.configurationtools.get_abjad_revision_string import get_abjad_revision_string
from abjad.tools.configurationtools.get_abjad_version_string import get_abjad_version_string


def _get_abjad_startup_string():

    return 'Abjad %s (r%s)' % (get_abjad_version_string(), get_abjad_revision_string())
