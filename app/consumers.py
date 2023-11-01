import json
from googletrans import Translator, LANGUAGES
import wave
from asgiref.sync import async_to_sync
from googletrans import Translator, LANGUAGES
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
import whisper
import os
from vosk import Model, KaldiRecognizer
import base64
from pydub import AudioSegment
from io import BytesIO

from .NER_models import Ner_Models

class TranslatorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Called on connection.
        # To accept the connection call:
       
        await self.accept()
        print("connet")
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        #self.accept("subprotocol")
        # To reject the connection, call:
        #self.close()

    async def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        ent1,ent2,labels1,labels2=[],[],[],[]
        Nermodel=Ner_Models()
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = whisper.load_model('base', device=device)
        text_data_json = json.loads(text_data)
        slang=text_data_json["from"]
        dstlang=text_data_json["to"]
        audio_base64_str = text_data_json.get('data').split(",")[1] # Get only the base64 content, removing the MIME type prefix.
        audio_bytes = base64.b64decode(audio_base64_str)  # Decode the base64 string to bytes

            # Save the audio bytes as a .wav file
   
        audio_file_path = 'aod.wav'
        with open(audio_file_path, 'wb') as f:
                f.write(audio_bytes)

        result = model.transcribe(audio_file_path, language=slang)
        os.remove(audio_file_path)

       
        
        translator = Translator()
        transl="translation does not complete try again . "
        if result["text"]:
            translation = translator.translate(result["text"], src=slang, dest=dstlang)
            transl=translation.text
            '''
        if slang =='en' :
            ent1,labels1=Nermodel.ner_es(result["text"])
        if dstlang=='en':
            ent2,labels2=Nermodel.ner_en(transl)
        if slang=='es':
            ent1,labels1=Nermodel.ner_es(result["text"])
        if dstlang=='es':
            ent2,labels2=Nermodel.ner_es(transl)
        if slang=='it':
            ent1,labels1=Nermodel.ner_it(result["text"])
        if dstlang=="it":
            ent2,labels2=Nermodel.ner_it(transl)
        if slang=='ar':
            ent1,labels1=Nermodel.ner_ar(result["text"])
        if dstlang=='ar':
            ent2,labels2=Nermodel.ner_ar(transl)

        '''
       

        
        await self.send(text_data=json.dumps({
                        'text':result["text"] ,
                        'translation': transl,
                         "speechHighlitedWords":{
                            "labels":labels1,
                            "entity":ent1
                         },
                        "highlightedWords":{
                            "label":labels2,
                            "entity":ent2
                        }

                    }))
  
        
    
        

    async def disconnect(self, close_code):
        # Called when the socket closes
        await self.close()




class NerConsumer(WebsocketConsumer):
    def connect(self):
        # Called on connection.
        # To accept the connection call:
        self.accept()
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        #self.accept("subprotocol")
        # To reject the connection, call:
        #self.close()

    def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        
        text = text_data_json["text"]
       # entities,labels=ner_en(text)
       # sentObject={}
       # self.send(text_data=json.dumps(sentObject))
        

    def disconnect(self, close_code):
        # Called when the socket closes
        self.close()
    
   # def ner_en( text):
            #tagger = SequenceTagger.load("flair/ner-english")
           # sentence = Sentence(text)
           # pred = tagger.predict(sentence)
            #entities, labels = [], []
           # for entity in sentence.get_spans('ner'):
            #    entities.append(entity.text)
            #    labels.append(entity.labels[0].value)
            #return entities, labels

