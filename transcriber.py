import json
import logging
import shlex
import subprocess

from vosk import KaldiRecognizer, Model
from timeit import default_timer as timer

from extractor import NumberExtractor

CHUNK_SIZE = 4000
SAMPLE_RATE = 16000.0
extractor = NumberExtractor()

class Transcriber:

    def __init__(self, model_dir_path):
        self.model = Model(model_path=model_dir_path)

    def recognize_stream(self, rec, stream):
        tot_samples = 0
        result = []
        while True:
            data = stream.stdout.read(CHUNK_SIZE)
            if len(data) == 0:
                break

            tot_samples += len(data)

            if rec.AcceptWaveform(data):
                jres = json.loads(rec.Result())
                result.append(jres)

            else:
                jres = json.loads(rec.PartialResult())
        jres = json.loads(rec.FinalResult())
        result.append(jres)
        processed_result = ""
        for part in result:
            if part["text"] != "":
                processed_result += part["text"] + " "

        return processed_result, tot_samples

    def resample_ffmpeg(self, infile):
        cmd = shlex.split("ffmpeg -nostdin -loglevel quiet "
                          "-i \'{}\' -ar {} -ac 1 -f s16le -".format(str(infile), SAMPLE_RATE))
        stream = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        return stream

    def pool_worker(self, inputdata):
        start_time = timer()

        try:
            stream = self.resample_ffmpeg(inputdata)
        except FileNotFoundError as e:
            print(e, "Missing FFMPEG, please install and try again")
            return
        except Exception as e:
            logging.info(e)
            return

        rec = KaldiRecognizer(self.model, SAMPLE_RATE)
        rec.SetWords(True)
        result, tot_samples = self.recognize_stream(rec, stream)
        if tot_samples == 0:
            return

        elapsed = timer() - start_time
        print("Execution time: {:.3f} sec".format(elapsed))
        text, mask = extractor.replace(result, apply_regrouping=True)
        return text

