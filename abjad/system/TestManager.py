import difflib
import os
import pathlib
from abjad.system.AbjadObject import AbjadObject


class TestManager(AbjadObject):
    """
    Manages test logic.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    __slots__ = (
        )

    ### PRIVATE METHODS ###

    @staticmethod
    def _compare_backup(path):
        if isinstance(path, str):
            paths = [path]
        elif isinstance(path, pathlib.Path):
            paths = [str(path)]
        elif (isinstance(path, (tuple, list))):
            paths = [str(_) for _ in path]
        else:
            raise TypeError(path)
        for path in paths:
            backup_path = path + '.backup'
            if not TestManager.compare_files(path, backup_path):
                return False
        return True

    @staticmethod
    def _compare_lys(path_1, path_2):
        """
        Compares LilyPond file ``path_1`` to LilyPond file ``path_2``.

        Performs line-by-line comparison.

        Discards blank lines.

        Discards any LilyPond version statements.

        Discards any lines beginning with ``%``.

        Returns true or false.
        """
        file_1_lines = TestManager._normalize_ly(path_1)
        file_2_lines = TestManager._normalize_ly(path_2)
        return file_1_lines == file_2_lines

    @staticmethod
    def _compare_text_files(path_1, path_2):
        """
        Compares text file ``path_1`` to text file ``path_2``.

        Performs line-by-line comparison.

        Discards blank lines.

        Trims whitespace from the end of each line.

        Returns true or false.
        """
        file_1_lines, file_2_lines = [], []
        with open(path_1, 'r') as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == '':
                    continue
                file_1_lines.append(line)
        with open(path_2, 'r') as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == '':
                    continue
                file_2_lines.append(line)
        return file_1_lines == file_2_lines

    @staticmethod
    def _normalize_ly(path):
        lines = []
        with open(path, 'r') as file_pointer:
            for line in file_pointer.readlines():
                line = line.strip()
                if line == '':
                    continue
                if line.startswith(r'\version'):
                    continue
                elif line.startswith('%'):
                    continue
                lines.append(line)
        return lines

    ### PUBLIC METHODS ###

    @staticmethod
    def compare(string_1, string_2):
        """
        Compares ``string_1`` to ``string_2``.

        Massage newlines.

        Returns true or false.
        """
        if not isinstance(string_1, str):
            string_1 = format(string_1)
        split_lines = string_2.split('\n')
        if not split_lines[0] or split_lines[0].isspace():
            split_lines.pop(0)
        if not split_lines[-1] or split_lines[-1].isspace():
            split_lines.pop(-1)
        indent_width = 0
        if split_lines:
            for indent_width, character in enumerate(split_lines[0]):
                if character != ' ':
                    break
        massaged_lines = []
        for split_line in split_lines:
            massaged_line = split_line[indent_width:]
            massaged_lines.append(massaged_line)
        massaged_string = '\n'.join(massaged_lines)
        return string_1.replace('\t', '    ') == massaged_string

    @staticmethod
    def compare_files(path_1, path_2):
        """
        Compares file ``path_1`` to file ``path_2``.

        For all file types::

        * Performs line-by-line comparison
        * Discards blank lines

        For LilyPond files, additionally::

        * Discards any LilyPond version statements
        * Discards any lines beginning with ``%``

        Returns true when files compare the same and false when files compare
        differently.
        """
        path_1 = str(path_1)
        path_2 = str(path_2)
        if os.path.exists(path_1) and not os.path.exists(path_2):
            return False
        elif not os.path.exists(path_1) and os.path.exists(path_2):
            return False
        elif not os.path.exists(path_1) and not os.path.exists(path_2):
            return True
        if path_1.endswith('.backup'):
            path_1 = path_1.strip('.backup')
        if path_2.endswith('.backup'):
            path_2 = path_2.strip('.backup')
        base_1, extension_1 = os.path.splitext(path_1)
        base_2, extension_2 = os.path.splitext(path_2)
        assert extension_1 == extension_2
        if extension_1 == '.ly':
            return TestManager._compare_lys(path_1, path_2)
        else:
            return TestManager._compare_text_files(path_1, path_2)

    @staticmethod
    def compare_objects(object_one, object_two):
        """
        Compares ``object_one`` to ``object_two``.

        Returns true or false.
        """
        import abjad
        agent_one = abjad.StorageFormatManager(object_one)
        if agent_one.format_specification.coerce_for_equality:
            try:
                object_two = type(object_one)(object_two)
            except (
                TypeError,
                ValueError,
                ):
                return False
        elif not isinstance(object_two, type(object_one)):
            return False
        agent_two = abjad.StorageFormatManager(object_two)
        template_1 = agent_one.get_template_dict()
        template_2 = agent_two.get_template_dict()
        return template_1 == template_2

    @staticmethod
    def diff(object_a, object_b, title=None):
        """
        Gets diff of ``object_a`` and ``object_b`` formats.

        >>> one = abjad.Flute()

        >>> two = abjad.BassFlute()

        >>> diff = abjad.TestManager.diff(one, two, 'Diff:')
        >>> print(diff)
        Diff:
        - abjad.Flute(
        + abjad.BassFlute(
        ?       ++++
        -     name='flute',
        +     name='bass flute',
        ?           +++++
        -     short_name='fl.',
        +     short_name='bass fl.',
        ?                 +++++
              markup=abjad.Markup(
        -         contents=['Flute'],
        ?                    ^
        +         contents=['Bass flute'],
        ?                    ^^^^^^
                  ),
              short_markup=abjad.Markup(
        -         contents=['Fl.'],
        ?                    ^
        +         contents=['Bass fl.'],
        ?                    ^^^^^^
                  ),
              allowable_clefs=('treble',),
              context='Staff',
        -     middle_c_sounding_pitch=abjad.NamedPitch("c'"),
        ?                                              ^  -
        +     middle_c_sounding_pitch=abjad.NamedPitch('c'),
        ?                                              ^
        -     pitch_range=abjad.PitchRange('[C4, D7]'),
        ?                                     ^  ^^
        +     pitch_range=abjad.PitchRange('[C3, C6]'),
        ?                                     ^  ^^
        -     primary=True,
              )

        Returns string.
        """
        try:
            a_format = format(object_a, 'storage')
        except ValueError:
            a_format = format(object_a)
        try:
            b_format = format(object_b, 'storage')
        except ValueError:
            b_format = format(object_b)
        a_format = a_format.splitlines(True)
        b_format = b_format.splitlines(True)
        diff = ''.join(difflib.ndiff(a_format, b_format))
        if title is not None:
            diff = title + '\n' + diff
        return diff
