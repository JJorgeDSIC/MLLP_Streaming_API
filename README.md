# [MLLP](https://www.mllp.upv.es/) Streaming API example

This repository contains some examples of client code to use the [MLLP](https://www.mllp.upv.es/) Streaming Speech Recognition API

## Setup and installation

Streaming API example, tested in Ubuntu 16.04 and Python3.6

System dependencies:

```bash
sudo apt install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools
```

Installation

```bash
#Prepare virtual environment
virtualenv env --python=/path/to/python3.6 env

#Activate environment
source env/bin/activate

#Install requirements
pip install -r requirements.txt

#Download & Install Streaming client library
wget https://ttp.mllp.upv.es/mllp-streaming-api/MLLPStreamingClient_mllp-1.0.0-py3-none-any.whl
pip install MLLPStreamingClient_mllp-1.0.0-py3-none-any.whl
```

## Examples

Replace this lines in the examples with your credentials and server information:

```python
server_hostname = "<SERVER_ADDRESS>"
server_port = "<PORT>"
api_user = "<YOU_API_USER>"
api_secret = "<YOUR_API_KEY>"
server_ssl_cert_file = "<CRT_FILE>"
```

To get the server SSL cert, use this commands:

```bash
apt-get install openssl
echo -n | openssl s_client -connect ttp.mllp.upv.es:443 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p' > ttp.mllp.upv.es.crt
```

To run the examples:

```bash
#Activate the environment
sourve env/bin/activate

#Sending WAV file
python3 python_examples/client.short.wav.py wav_example/AAFA0016.wav

#Sending audio from mic
python3 python_examples/client.mic.py
```

## Detailed documentation (login required):

* [Streaming service API](https://ttp.mllp.upv.es/index.php?page=api) (login required)
* [Python API client](https://ttp.mllp.upv.es/mllp-streaming-api/MLLPStreamingClient.html)

## Contact and support

mail: mllp-support@upv.es

