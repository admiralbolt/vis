import json
import random
import time
from typing import Any

import numpy as np

from pipe_client import PipeClient

class Field:

  name: str
  
  def __init__(self):
    pass

  def get_value(self, chaos: float) -> Any:
    """Should be overriden in child."""
    pass


  def to_string(self, chaos: float):
    return f"{self.name}={self.get_value(chaos=chaos)}"

class IntField(Field):

  def __init__(self, name: str, min_range: int, max_range: int):
    self.name = name
    self.min_range = min_range
    self.max_range = max_range

  def get_value(self, chaos: float) -> int:
    midpoint = (self.max_range - self.min_range) / 2
    sigma = (chaos / 10) * midpoint
    val = int(random.gauss(midpoint, sigma))
    return max(min(val, self.max_range), self.min_range)


class DoubleField(Field):

  def __init__(self, name: str, min_range: float, max_range: float):
    self.name = name
    self.min_range = min_range
    self.max_range = max_range

  def get_value(self, chaos: float) -> int:
    midpoint = (self.max_range - self.min_range) / 2
    sigma = (chaos / 10) * midpoint
    val = random.gauss(midpoint, sigma)
    return max(min(val, self.max_range), self.min_range)

class SelectionField(Field):

  def __init__(self, name: str, choices: list[str]):
    self.name = name
    self.choices = choices

  def get_value(self, chaos: float) -> str:
    return f"'{random.choice(self.choices)}'"


class Effect:

  fields: list[Field]

  def __init__(self, name: str):
    self.name = name
    self.fields = []

  def add_field(self, field: Field) -> None:
    self.fields.append(field)

  def get_effect_command(self, chaos: float) -> str:
    effect_string = " ".join([f"'{field.name}'={field.get_value(chaos=chaos)}" for field in self.fields])
    return f"{self.name}: {effect_string}"


# Reverb: RoomSize=100 Reverberance=100 WetGain=3

reverb = Effect("Reverb")
reverb.add_field(DoubleField(name="RoomSize", min_range=0, max_range=100))
reverb.add_field(DoubleField(name="Reverberance", min_range=0, max_range=100))
reverb.add_field(IntField(name="Delay", min_range=0, max_range=200))
reverb.add_field(IntField(name="ToneLow", min_range=0, max_range=100))
reverb.add_field(IntField(name="ToneHigh", min_range=0, max_range=100))
reverb.add_field(IntField(name="Damping", min_range=0, max_range=100))

bass_and_treble = Effect("BassAndTreble")
bass_and_treble.add_field(DoubleField(name="Bass", min_range=-5, max_range=5))
bass_and_treble.add_field(DoubleField(name="Treble", min_range=-5, max_range=5))

pitch_change = Effect("ChangePitch")
pitch_change.add_field(DoubleField(name="Percentage", min_range=-8, max_range=8))

distortion = Effect("Distortion")
distortion.add_field(SelectionField(name="Type", choices=[
  "Hard Clipping",
  "Soft Clipping",
  "Soft Overdrive",
  "Medium Overdrive",
  "Hard Overdrive",
  "Cubic Curve",
  "Even Harmonics",
  "Expand and Compress",
  "Leveller",
  "Rectifier Distortion",
  "Hard Limiter 1413"
]))
distortion.add_field(DoubleField(name="Parameter 1", min_range=0, max_range=100))
distortion.add_field(DoubleField(name="Parameter 2", min_range=0, max_range=100))

echo = Effect("Echo")
echo.add_field(DoubleField(name="Delay", min_range=0.5, max_range=3))
echo.add_field(DoubleField(name="Decay", min_range=0.5, max_range=1.3))

phaser = Effect("Phaser")
phaser.add_field(IntField(name="DryWet", min_range=0, max_range=255))
phaser.add_field(DoubleField(name="Freq", min_range=0.5, max_range=4))
phaser.add_field(IntField(name="Depth", min_range=0, max_range=255))

wahwah = Effect("Wahwah")
wahwah.add_field(DoubleField(name="Freq", min_range=0.5, max_range=4))
wahwah.add_field(IntField(name="Depth", min_range=0, max_range=100))
wahwah.add_field(DoubleField(name="Resonance", min_range=0.5, max_range=10))


class ChaosKnob:

  effects: list[Effect]

  def __init__(self):
    self.effects = [
      reverb, pitch_change, distortion, echo, phaser, wahwah
    ]
    self.client = PipeClient()
    self.client.write("GetInfo: Type=Tracks")
    time.sleep(2)
    track_info_raw = self.client.read()
    track_info_raw = "\n".join(track_info_raw.split("\n")[:-2])
    print("---")
    print(track_info_raw)
    print("---")
    self.track_info = json.loads(track_info_raw)


  def do_it(self, chaos: float) -> None:
    for _ in range(int(chaos) * 6):
      self.apply_random_effect(chaos=chaos)
      time.sleep(0.2)

  def apply_random_effect(self, chaos: float) -> None:
    i = random.randint(0, len(self.track_info) - 1)
    track = self.track_info[i]
    # 1) Select the track in question.
    self.client.write(f"SelectTracks: Track={i} Mode=Set")
    # 2) Select a random time range within the track.
    min_time = track["start"]
    max_time = track["end"]
    time_slice = np.random.lognormal(0, chaos / 10) * (max_time - min_time) / 4
    start_time = random.uniform(min_time, max_time)
    end_time = min(max_time, start_time + time_slice)
    self.client.write(f"SelectTime: Start={start_time} End={end_time}")
    # 3) Apply our effect!
    effect = random.choice(self.effects)
    self.client.write(effect.get_effect_command(chaos=chaos))


if __name__ == "__main__":
  chaos_knob = ChaosKnob()
  chaos_knob.do_it(chaos=10)

  while True:
    pass
