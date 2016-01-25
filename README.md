# adom-generator
````
git clone git@github.com:yhal003/adom-generator.git
cd adom-generator
sudo docker build --no-cache -t adom .


sudo docker run -ti -v \
  `pwd`/conf/charConf.py:/root/adom_bot/charConf.py -v \
  `pwd`/test:/root/.adom.data/savedg adom
````
