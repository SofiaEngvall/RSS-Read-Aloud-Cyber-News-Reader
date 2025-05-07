# linux_speaker.py - Class to simplify use of gTTS for TTS on Linux
# version 1.1
# by Sofia Engvall - FixIt42, 2025-05-07

import os
import tempfile
from gtts import gTTS
import subprocess

VOICE = 'en'   # gTTS uses language codes instead of numbered voices
SPEED = 1.0    # 1.0 is normal, <1 is slower, >1 is faster (equivalent to Windows TTS speed range)

class Speaker():
    def __init__(self, also_print=False, speed=SPEED):
        self.voice = VOICE
        self.speed = speed
        self.also_print = also_print
        # self.print_voices()  # Not applicable in gTTS
        self.set_speed(speed)

    def set_voice(self, voice_code):
        self.voice = voice_code

    def print_voices(self):
        print("gTTS uses Google Translate voices (limited), typically:")
        print("- 'en', 'en-us', 'en-uk', 'sv', 'de', 'fr', etc.")

    def set_speed(self, speed):
        # Adjust the speed to match Windows rate
        # Windows rate: -10 to 10, where 0 is normal
        if speed < -10 or speed > 10:
            raise ValueError("Speed must be between -10 and 10.")
        
        # Mapping Windows speed (-10 to 10) to gTTS speed factor (0.5 to 2.0)
        # Example: speed=4 -> 1.3, speed=-4 -> 0.8
        self.speed = 1.0 + (speed / 10.0) * 1.0

    def tell_speed(self):
        self.speak(f"My speaking rate multiplier is set to {self.speed}.")

    def speak(self, text):
        if self.also_print:
            print(text)
        try:
            tts = gTTS(text=text, lang=self.voice)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                # Use ffplay to play and apply speed control (matching Windows-like speed behavior)
                subprocess.run(
                    ["ffplay", "-autoexit", "-nodisp", "-af", f"atempo={self.speed}", "-loglevel", "quiet", fp.name],
                    check=True
                )
            os.remove(fp.name)
        except Exception as e:
            print(f"Error in TTS: {e}")

if __name__ == "__main__":
    s = Speaker()
    s.print_voices()
