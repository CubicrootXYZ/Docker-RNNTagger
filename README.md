# Docker-RNNTagger
Docker Container as a wrapper for RNNTagger with easy to use API. You can watch the documentation for RNNTagger here: [Link](https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/).

## Installation

Because the license of RNNTagger forbids the redistribution of itself I am not able to share the docker image with you until I get a separate license. 

Unfortunately you have to build the container yourself with this easy steps:

1. Create a folder on your linux system with docker
2. Copy the `Dockerfile` there
3. Run in the same folder: `docker build --no-cache -t imagename` (change imagename to your desired image name

Afterwards you simply can run the container with `docker run -d -p 80:8080 imagename`. Change the port according to your needs. You might want to use docker compose for this.

## Endpoints

### GetTags

Tags all words and stemms them to their root word.

Url: `/gettags`

**Parameters (GET)**

lang: Language to tag

string: your text to stemm

**Returns**

Returns a List with sentences, sentences are lists with a dict for each word with `original`, `tag` and `root`.

### GetLangs

List all available languages.

Url: `/getlangs`

**Return**

Returns a list of languages available.
