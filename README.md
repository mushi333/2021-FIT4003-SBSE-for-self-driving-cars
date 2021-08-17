# **2021-FIT4003-SBSE-for-self-driving-cars**

### **Prerequisites**
- Python 3.7
- Configuration for Linux Ubuntu 20.04
- Git and pip installed

### **Steps to install python 3.7**
```
sudo apt update
pip install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.7
python3.7 --version
```
### **Steps to create a virtual environment**
```
mkdir python-env
sudo apt install virtualenv
cd python-env
virtualenv --python=python3.7 ast-env
ls ast-env/lib
source ast-env/bin/activate
```
### **Steps to install ast-toolbox for Linux**
``` 
cd ast-env
git clone https://github.com/sisl/AdaptiveStressTestingToolbox.git
cd AdaptiveStressTestingToolbox
git submodule update --init --recursive
sudo chmod a+x scripts/install_all.sh
```
change the contents of requirements.txt to new_req.txt
```
sudo scripts/install_all.sh
source scripts/setup.sh
sudo apt-get install libpython3.7-dev
pip install bsddb3
pip install torch==1.3.0+cpu torchvision==0.4.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install tensorflow==1.15.3
pip install dataclasses==0.6
pip install ast-toolbox
python setup.py install
```
follow step 5 & 6 in the tutorial of the documentation
