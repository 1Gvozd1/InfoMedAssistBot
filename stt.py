import json
import os
import asyncio
from vosk import Model, KaldiRecognizer
from extractor import NumberExtractor
import time

# model = Model("models/vosk/modelSmall")

class AsyncSTT:
    default_init = {
        "sample_rate": 16000,
        "ffmpeg_path": "models/vosk/ffmpeg"
    }

    def __init__(self):
        self.sample_rate = AsyncSTT.default_init["sample_rate"]
        self.ffmpeg_path = AsyncSTT.default_init["ffmpeg_path"]
        self.recognizer = KaldiRecognizer(model, self.sample_rate)
        self.recognizer.SetWords(True)

    async def audio_to_text(self, audio_file_name=None):
        if audio_file_name is None:
            raise Exception("Укажите путь и имя файла")
        if not os.path.exists(audio_file_name):
            raise Exception("Укажите правильный путь и имя файла")
        start_time = time.time()
        process = await asyncio.create_subprocess_exec(
            self.ffmpeg_path,
            "-loglevel", "quiet",
            "-i", audio_file_name,
            "-ar", str(self.sample_rate),
            "-ac", "1",
            "-f", "s16le",
            "-",
            stdout = asyncio.subprocess.PIPE
        )
        while True:
            data = await process.stdout.read(4000)
            if len(data) == 0:
                break
            if self.recognizer.AcceptWaveform(data):
                pass
        await process.wait()
        result_json = self.recognizer.FinalResult()
        result_dict = json.loads(result_json)
        extractor = NumberExtractor()
        text, mask = extractor.replace(result_dict["text"], apply_regrouping=True)
        print("--- %s seconds ---" % (time.time() - start_time))
        return text