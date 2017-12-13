apt-get update
apt install gcc python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev zlib1g-dev
cd ryu/
pip install --upgrade .
python setup.py install
