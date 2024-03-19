import requests

result = requests.post("http://localhost:11434/api/generate", json={
    "model": "key_Insighter", 
    "prompt": "If you want to set custom options for the model at runtime rather than in the Modelfile, you can do so with the options parameter. This example sets every available option, but you can set any of them individually and omit the ones you do not want to override.",
    "format": "json",
    "stream": False
})

response = result.json()

print(response)