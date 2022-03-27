#ubuntu commands
# create a separate environment using python-env
# install flask, sqlalchemy, requests

#activating server

cd AP086

source bin/activate

export FLASK_APP=apiCenter

exprot FLASK_DEBUG=1

flask run -h 0.0.0.0 -p 5000
