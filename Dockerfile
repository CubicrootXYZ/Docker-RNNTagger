FROM debian:latest
RUN apt update && apt install -y python3 python3-pip git unzip wget
RUN apt upgrade -y
RUN pip3 install --upgrade pip
RUN pip3 install torch
RUN pip3 install falcon gunicorn
RUN mkdir /opt/app
RUN wget "https://www.cis.uni-muenchen.de/~schmid/tools/RNNTagger/data/RNNTagger-1.2.zip" -P /opt/app
RUN mkdir /opt/app/RNNTagger
RUN unzip /opt/app/RNNTagger-1.2.zip -d /opt/app
RUN git clone https://github.com/CubicrootXYZ/Docker-RNNTagger.git /tmp/app
RUN mv /tmp/app/* /opt/app/RNNTagger/
RUN rm -R /tmp/app
RUN rm /opt/app/RNNTagger-1.2.zip

WORKDIR /opt/app/RNNTagger
ENTRYPOINT ["gunicorn", "docker_rnntagger:api",  "--workers 1",  "-b 0.0.0.0:8080",  "--reload"]
