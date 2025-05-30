from TTS.api import TTS
import soundfile as sf

VOICE = 'tts_models/en/ljspeech/tacotron2-DDC'
OUTPUT_FILE = 'output.wav'
SPEED = 1.0  # Normal speed; <1.0 = slower, >1.0 = faster

class Speaker():
    def __init__(self, also_print=False, speed=SPEED):
        self.also_print = also_print
        self.speed = speed
        self.tts = TTS(VOICE)

    def print_voices(self):
        print(f"Using voice/model: {VOICE}")

    def set_speed(self, speed):
        self.speed = speed

    def speak(self, text):
        if self.also_print:
            print(text)
        try:
            wav = self.tts.tts(text, speed=self.speed)
            sf.write(OUTPUT_FILE, wav, self.tts.synthesizer.output_sample_rate)
            import os
            os.system(f"aplay {OUTPUT_FILE}")
        except Exception as e:
            print(f"Error in TTS: {e}")

if __name__ == "__main__":
    s = Speaker()
    s.print_voices()
    s.set_speed(1.2)  # e.g., 20% faster
    s.speak("Hello! This is Coqui TTS speaking with adjustable speed on Linux.")
