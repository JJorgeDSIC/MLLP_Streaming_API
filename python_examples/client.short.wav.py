import json
import sys
from MLLPStreamingClient import MLLPStreamingClient

def main(wav):
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

    #Audio streaming iterator, sends audio in chunks of 250 bytes
    def myStreamIterator():
        with open(wav,"rb") as fd:
            data = fd.read(250)
            while data != b"":
                yield data
                data = fd.read(250)
                #Some delay to simulate mic input...
                time.sleep(0.0078125)

    es_system = {}

    #Select Spanish system for testing
    for system in systems:
        if system['info']['langs'][0]['code'] == "es":
            es_system = system

    if es_system == {}:
        raise Exception("Spanish system not found")

    
    for resp in cli.transcribe(es_system['id'], myStreamIterator):
        # Hyp_novar contains part of the hypothesis that is consolidated (hypothesis will not change)
        if resp["hyp_novar"] != "":
            sys.stdout.write("{} ".format(resp["hyp_novar"].strip()))
            if resp["eos"]:
                sys.stdout.write("\n")
            sys.stdout.flush()

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("client.short.wav.py <WAV>")
    else:
        main(sys.argv[1])
        
