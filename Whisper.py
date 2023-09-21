import threading

from faster_whisper import WhisperModel


class WhisperRecognizer:
    def __init__(self):
        self.model = WhisperModel("tiny", device="cpu", compute_type="int8")

    def transcribe(self, audio_file):
        segments, info = self.model.transcribe(audio_file, beam_size=5, language="ru", without_timestamps=True)
        print("out transcribe")
        result_string = ""
        for segment in segments:
            print(threading.get_ident(), segment.text)
            result_string += segment.text

        return result_string
