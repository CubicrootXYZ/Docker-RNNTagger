import subprocess, os, falcon, json
from falcon import uri

class GetTags():
    """Class for the tagging endpoint, receives text, tags it and sends everything back
    """
    def __init__(self):
        """actually doing nothing
        """
        pass

    def on_get(self, req, resp):
        """handles a get request on the /gettags endpoint

        Args:
            req (-): the request object
            resp (-): the response object
        """
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

    def on_post(self, req, resp):
        """handles a post request on the /gettags endpoint

        Args:
            req (-): the request object
            resp (-): the response object
        """
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

        files = os.listdir("/opt/app/RNNTagger/cmd")
        langs = []
        for f in files:
            if "rnn-tagger" in f:
                langs.append(f.replace("rnn-tagger-", "").replace(".sh", ""))

        try:
            data = json.loads(req.bounded_stream.read().decode("utf-8"))
            string = data["string"]
            lang = data["lang"]
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
    """class for handling the language endpoint
    """
    def __init__(self):
        """another empty function
        """
        pass

    def on_get(self, req, resp):
        """handles get requests on the /getlangs endpoint

        Args:
            req (-): request object
            resp (-): response object
        """
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', 'GET')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')

        files = os.listdir("/opt/app/RNNTagger/cmd")
        langs = []
        for f in files:
            if "rnn-tagger" in f:
                langs.append(f.replace("rnn-tagger-", "").replace(".sh", ""))
        
        resp.body = json.dumps({"languages": langs})

# create an instance and all endpoints
api = falcon.API()
#api.req_options.auto_parse_from_urlencoded = True
api.add_route('/gettags', GetTags())
api.add_route('/getlangs', GetLangs())
