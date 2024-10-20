from TTS.api import TTS
# import sounddevice as sd
import torch
import time
import sys
import numpy as np


class TTSGame:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
    
        self.speakers = self.tts.speakers
        self.speaker = self.speakers[0]

    # def play_wav(self,sample,emotion=None,rate=22050):
    #     rate = 1.2* rate
    #     wav = self.tts.tts(text=sample, language="en", speaker=self.speaker,emotion=emotion)
    #     sd.play(wav, samplerate=rate)
    #     sd.wait()
        
    # def streaming(self,sentances):
    #     for sentance in sentances:
    #         print(sentance)
    #         self.play_wav(sample=sentance)

    def save_wav(self,sample,path):
        wav = self.tts.tts_to_file(text=sample,speaker=self.speaker,language='en',file_path=path)
        return wav

    def get_wav(self,sample,emotion=None,rate=22050):
        wav = self.tts.tts(text=sample, language="en", speaker=self.speaker,emotion=emotion)
        return wav

    def list_speakers(self):
        print(f'Speakers count: {len(self.speakers)}')
        for i, speaker in enumerate(self.speakers):
            print(f'{i}: {speaker}')

    def change_speaker(self, speaker_index: int):
        if 0 <= speaker_index < len(self.speakers):
            self.speaker = self.speakers[speaker_index]
            print(f'Speaker changed to: {self.speaker}')
        else:
            print(f'Invalid speaker index. Please select a number between 0 and {len(self.speakers) - 1}.')


if __name__=='__main__':
    tts = TTSGame()
    wav = tts.get_wav(sample='Hello World!')
    print(wav)
    # sentences = ["This is sentence one.", "Here is sentence two.", "Now comes sentence three."]

    # tts.streaming(sentances=sentences)


   
    


