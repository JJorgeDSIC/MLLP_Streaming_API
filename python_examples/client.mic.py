import json
import pyaudio
import sys
from MLLPStreamingClient import MLLPStreamingClient

server_hostname = "<SERVER_ADDRESS>"
server_port = "<PORT>"
api_user = "<YOU_API_USER>"
api_secret = "<YOUR_API_KEY>"
server_ssl_cert_file = "<CRT_FILE>"

#Client object creation
cli = MLLPStreamingClient(server_hostname, server_port, api_user,api_secret, server_ssl_cert_file)
#Get Token for the session
cli.getAuthToken()
#Get available systems, a dictionary with the information related to the available systems and languages
systems = cli.getTranscribeSystemsInfo()

#Audio streaming iterator to send the audio file
def myStreamIterator():
    #Audio features
    CHUNK = 1024
    #1 channel, 16Khz, int16 audio
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    #Limits the recording to 120 seconds
    RECORD_SECONDS = 120
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=CHUNK)

    print("Sending data..")
    #Sends data in chunks of 1024 bytes
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        yield data
    #Stops and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

es_system = {}

#Select Spanish system for testing
for system in systems:
    if system['info']['langs'][0]['code'] == "es":
        es_system = system    

if es_system == {}:
    raise Exception("Spanish system not found") 
        
#Selects the system with the system id for the Spanish system, updated in Feb20
for resp in cli.transcribe(es_system, myStreamIterator):
    # Hyp_var contains part of the hypothesis that is not consolidated yet (hypothesis could change)
    if resp["hyp_var"] != "":
        print("VAR")
        sys.stdout.write("{} ".format(resp["hyp_var"].strip().replace("[SILENCE]","")))
        if resp["eos"]:
            sys.stdout.write("\n")
        sys.stdout.flush()
    # Hyp_novar contains part of the hypothesis that is consolidated (hypothesis will not change)
    if resp["hyp_novar"] != "":
        print("\nNOVAR")
        sys.stdout.write("{} ".format(resp["hyp_novar"].strip()))
        if resp["eos"]:
            sys.stdout.write("\n")
        sys.stdout.flush()


