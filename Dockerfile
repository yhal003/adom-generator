FROM ubuntu
COPY adom59 /root/adom59
COPY adom_bot /root/adom_bot
COPY GateOne /root/GateOne
COPY .adom.data /root/.adom.data
RUN sudo apt-get update
RUN sudo apt-get install -y python3-pip
RUN sudo pip3 install vt102 && sudo pip3 install pyte && sudo pip3 install profilehooks
WORKDIR /root/GateOne
RUN python3 setup.py install
WORKDIR /root/adom_bot
RUN timeout 1 python3 generator.py 10 charConf.py || echo hello
ENTRYPOINT ["python3","generator.py"]
CMD ["10000","charConf.py"]
VOLUME /root/.adom.data/savedg

