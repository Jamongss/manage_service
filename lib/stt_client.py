#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""program"""
__author__ = "Mindslab"
__date__ = "2020-03-24"
__last_modified_by__ = "Jamongss"
__last_modified_date__ = "2025-10-04"
__maintainer__ = "Jamongss"

###########
# imports #
###########
import os
import sys
import grpc
import traceback
# sys.path.append(os.path.join(os.getenv('MAUM_ROOT'), 'lib/python'))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from maum.brain.w2l import w2l_pb2_grpc
from maum.brain.w2l import w2l_pb2

#########
# class #
#########
class SttClient(object):
    def __init__(self, remote='127.0.0.1:15001', chunk_size=64*1024):
        try:
            self.channel = grpc.insecure_channel(remote)
            self.stub = w2l_pb2_grpc.SpeechToTextStub(self.channel)
            self.chunk_size = chunk_size
        except Exception:
            print(traceback.format_exc())

    def recognize(self, wav_binary):
        wav_binary = self._generate_wav_binary_iterator(wav_binary)
        return self.stub.Recognize(wav_binary)

    def _generate_wav_binary_iterator(self, wav_binary):
        for idx in range(0, len(wav_binary), self.chunk_size):
            yield w2l_pb2.Speech(bin=wav_binary[idx:idx + self.chunk_size])

    @staticmethod
    def bytes_from_file(pcm_file_path, chunksize=10000):
        with open(pcm_file_path, "rb") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    speech = w2l_pb2.Speech()
                    speech.bin = chunk
                    yield speech
                else:
                    break

    def stream_recognize(self, pcm_file_path):
        try:
            segments = self.stub.StreamRecognize(self.bytes_from_file(pcm_file_path))
            output_list = list()
            for seg in segments:
                output_list.append(seg)
            return output_list
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            # print('StreamReconize() failed with {0}: {1}'.format(e.code(), e.details()))

    def disconnect(self):
        try:
            print("STT grpc session closed ..")
            self.channel.close()
            print("Successfully disconnected from the grpc session ..")
        except Exception:
            print(traceback.format_exc())


########
# main #
########
if __name__ == '__main__':
    try:
        remote = 'localhost:15999'
        client = SttClient(remote)
        results = client.stream_recognize('test.pcm')
        for result in results:
            print('{0}\t{1}\t{2}'.format(result.start / 80.0, result.end / 80.0, result.txt))
        # client.disconnect()
    except Exception:
        print(traceback.format_exc())

