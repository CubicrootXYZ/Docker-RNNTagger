import subprocess, os, falcon, json
from falcon import uri

class GetTags():
    def __init__(self):
        pass

    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

        files = os.listdir("/opt/app/RNNTagger/cmd")
        langs = []
        for f in files:
            if "rnn-tagger" in f:
                langs.append(f.replace("rnn-tagger-", "").replace(".sh", ""))

        try:
            string = req.params["string"]
            lang = req.params["lang"]
            f = open("/opt/app/RNNTagger/test.txt", "w")
            f.write(string)
            f.close()
            if len(string) < 2:
                error="No text given"
            if lang not in langs:
                error="Language not available"
            process = subprocess.Popen("./cmd/rnn-tagger-"+lang+".sh ./test.txt", stdout=subprocess.PIPE, shell=True)
            output, error = process.communicate()
        except Exception as e:
            error=e

        if error is None:
            output = output.decode("utf-8")
            output = output.split("\n")

            tagged = []

            sentence = []
            for sen in output:
                if len(sen) == 0:
                    tagged.append(sentence)
                    sentence=[]
                sen = sen.split("\t")
                if len(sen) != 3:
                    continue
                
                sentence.append({"original": sen[0], "tag": sen[1], "root": sen[2]})

            tagged.append(sentence)
            tagged = [x for x in tagged if x != []]
            resp.body = json.dumps(tagged)
        else:
            resp.body = json.dumps({"status": "error occured", "error": str(error)}) 

class GetLangs():
    def __init__(self):
        pass

    def on_get(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

        files = os.listdir("/opt/app/RNNTagger/cmd")
        langs = []
        for f in files:
            if "rnn-tagger" in f:
                langs.append(f.replace("rnn-tagger-", "").replace(".sh", ""))
        
        resp.body = json.dumps({"languages": langs})

api = falcon.API()
api.add_route('/gettags', GetTags())
