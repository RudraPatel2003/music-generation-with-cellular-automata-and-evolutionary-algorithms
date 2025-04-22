from music21 import stream, chord, scale, midi
from cellular_automata.cellular_automata import CellularAutomata


class MusicPlayer:
    def __init__(self, automata: CellularAutomata):
        self.history = automata.get_history()

    def play(self):
        steam = stream.Stream()

        pitches = scale.MajorScale("C").getPitches("C3", "C5")

        for time_step in self.history:
            time_step_chord = chord.Chord(
                [note for note, is_played in zip(pitches, time_step) if is_played]
            )
            time_step_chord.duration.quarterLength = 0.5
            steam.append(time_step_chord)

        player = midi.realtime.StreamPlayer(steam)
        player.play()
