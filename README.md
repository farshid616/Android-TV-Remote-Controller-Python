# androidTV-controller-Python
Simple Python program that communicate with android TV through network to pair with TV and will control it over the network.

Works on Mi box and some of android TVs.

Special thanks to [@Aymkdn](https://github.com/Aymkdn) for his detailed wiki. For protocol details check [here](https://github.com/Aymkdn/assistant-freebox-cloud/wiki/Google-TV-(aka-Android-TV)-Remote-Control).

## Tested on:
```
Mi Box4
```

## Requirements: 
* python3
* pynput
* cryptography
* pyOpenSSL
* asn1crypto

## prepair and run:
After Installing requirements you should generate certificate and pair your client to the server.

```
$ pip3 install -r requirements.txt
$ python3 certificate_generator.py
$ python3 android_tv_remote.py pairing
```

After first time pairing, you can run it without pairing argument.
