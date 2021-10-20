import dataclasses

from .. import bundle as _bundle


@dataclasses.dataclass
class BeamCount:
    r"""
    LilyPond ``\setLeftBeamCount``, ``\setRightBeamCount`` command.

    ..  container:: example

        >>> abjad.BeamCount()
        BeamCount(left=0, right=0)

    """

    left: int = 0
    right: int = 0

    _is_dataclass = True

    def _get_lilypond_format_bundle(self, component=None):
        bundle = _bundle.LilyPondFormatBundle()
        string = rf"\set stemLeftBeamCount = {self.left}"
        bundle.before.commands.append(string)
        string = rf"\set stemRightBeamCount = {self.right}"
        bundle.before.commands.append(string)
        return bundle
