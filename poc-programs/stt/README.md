```
pip3 install --upgrade google-cloud-speech
```


```
python3 -m venv ~/stt-venv
source ~/stt-venv/bin/activate
pip install google-cloud-speech
```

Get operation status:

```
curl -X GET -H "Authorization: Bearer $(gcloud auth print-access-token)"  \
    -H "x-goog-user-project: ${PROJECT_ID}" \
    "https://${LOCATION}-speech.googleapis.com/v2/projects/${PROJECT_ID}/locations/us/operations/v2-xxxx-xxxx-xxxx-xxxx-xxxx
```

STT Console UI:
http://g.co/cloud/speech-ui