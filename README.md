# adom-generator

To build:
````
git clone git@github.com:yhal003/adom-generator.git
cd adom-generator
sudo docker build --no-cache -t adom .
````

To run: 
````
sudo docker run -ti -v \
  `pwd`/conf/charConf.py:/root/adom_bot/charConf.py -v \
  `pwd`/test:/root/.adom.data/savedg adom
````

 `pwd`/conf/charConf.py is a path to character description, have a a look in conf directory for examples. `pwd`/test is where you want save files to be stored. 
 
 To run in background replace '-ti' with '-td'.
