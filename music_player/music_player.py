from music21 import stream, chord, scale
from cellular_automata.cellular_automata import CellularAutomata
import subprocess

SOUNDFONT_PATH = "music_player/soundfont.sf2"
MIDI_PATH = "temp/midi_file.mid"
WAV_PATH = "temp/wav_file.wav"
MP3_PATH = "temp/mp3_file.mp3"


class MusicPlayer:
    def __init__(self, automata: CellularAutomata):
        self.history = automata.get_history()
        self.stream = self.generate_stream()

    def generate_stream(self):
        s = stream.Stream()

        pitches = scale.MajorScale("C").getPitches("C3", "C5")

        for time_step in self.history:
            time_step_chord = chord.Chord(
                [note for note, is_played in zip(pitches, time_step) if is_played]
            )
            time_step_chord.duration.quarterLength = 0.5
            s.append(time_step_chord)

        return s

    def export_as_mp3(self):
        self.stream.write("midi", fp=MIDI_PATH)

        subprocess.run(
            [
                "fluidsynth",
                "-ni",
                SOUNDFONT_PATH,
                MIDI_PATH,
                "-F",
                WAV_PATH,
                "-r",
                "44100",
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

        subprocess.run(
            ["ffmpeg", "-y", "-i", WAV_PATH, MP3_PATH],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )

        return MP3_PATH
