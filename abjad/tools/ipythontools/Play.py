# -*- coding: utf-8 -*-
import os
import shutil
import tempfile


class Play(object):
    r'''IPython replacement callable for `topleveltools.show()`.

    Integrates audio rendering of Abjad MIDI files into IPython notebooks
    using `timidity`.
    '''

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        '''Render `expr` as Vorbis audio and display it in the IPython notebook
        as an <audio> tag.
        '''
        from abjad.tools import systemtools
        from abjad.tools import topleveltools
        assert hasattr(expr, '__illustrate__')
        if not systemtools.IOManager.find_executable('timidity'):
            message = 'WARNING: timidity is not available; '
            message += 'cannot render MIDI file to OGG.'
            print(message)
            return
        temp_directory = tempfile.mkdtemp()
        midi_file_path = os.path.join(temp_directory, 'out.mid')
        result = topleveltools.persist(expr).as_midi(midi_file_path)
        midi_file_path, format_time, render_time = result
        ogg_file_path = os.path.join(temp_directory, 'out.ogg')
        encoded_audio = self._get_ogg_as_base64(
            midi_file_path,
            ogg_file_path,
            )
        if encoded_audio is not None:
            self._display_ogg_audio_tag(encoded_audio)
        shutil.rmtree(temp_directory)

    ### PRIVATE METHODS ###

    def _display_ogg_audio_tag(self, encoded_audio):
        from IPython.core.display import display_html
        audio_tag = '<audio controls type="audio/ogg" '
        audio_tag += 'src="data:audio/ogg;base64,{}">'
        audio_tag = audio_tag.format(encoded_audio)
        display_html(audio_tag, raw=True)

    def _get_base64_from_file(self, file_name):
        '''Read the base64 representation of a file and encode for HTML.
        '''
        import base64
        with open(file_name, 'rb') as file_pointer:
            data = file_pointer.read()
            return base64.b64encode(data).decode('utf-8')

    def _get_ogg_as_base64(
        self,
        midi_file_path,
        ogg_file_path,
        ):
        from abjad.tools import systemtools
        command = 'timidity {midi_file_path} -Ov -o {ogg_file_path}'.format(
            midi_file_path=midi_file_path,
            ogg_file_path=ogg_file_path,
            )
        result = systemtools.IOManager.spawn_subprocess(command)
        if result == 0:
            encoded_audio = self._get_base64_from_file(ogg_file_path)
            return encoded_audio
        message = 'timidity failed to render MIDI as OGG, result: {}'
        message = message.format(result)
        print(message)
        return None

    ### PUBLIC METHODS ###

    def load_sound_font(self, new_sound_font, new_midi_bank):
        '''Save location of argument sound_font and its type.

        Type can be either 'gs', 'gm', 'xg', or 'mma'.
        '''
        new_sound_font = os.path.expanduser(new_sound_font)
        if os.path.isfile(new_sound_font):
            self._sound_font = new_sound_font
        else:
            message = 'The specified sound_font {} (relative to {}) '
            message += 'is either inaccessible or does not exist.'
            message = message.format(new_sound_font, os.getcwd())
            print(message)
        valid_midi_banks = ('gs', 'gm', 'xg', 'mma')
        if new_midi_bank in valid_midi_banks:
            self._midi_bank = new_midi_bank
        else:
            message = 'The MIDI bank must be either be one of {!s}'
            message = message.format(valid_midi_banks)
            print(message)

    ### PUBLIC PROPERTIES ###

    @property
    def midi_bank(self):
        r'''Gets midi bank name.

        Returns string.
        '''
        return self._midi_bank

    @property
    def sound_font(self):
        r'''Gets sound font path.

        Returns string.
        '''
        return self._sound_font
