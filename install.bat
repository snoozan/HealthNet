ECHO ON
python get-pip.py --user
pip install --user -r requirements.txt
python healthnet/manage.py migrate
python manage.py runserver
