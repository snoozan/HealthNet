ECHO ON
python get-pip.py --user
pip install --user -r requirements.txt
python manage.py migrate
python manage.py runserver
