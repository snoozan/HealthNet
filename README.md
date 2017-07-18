# Health Net

## Migration directions
```
python manage.py migrate users 0001_initial
python manage.py loaddata users/fixtures/hospital.json
python manage.py loaddata users/fixtures/usersPermissions.json
python migrate
```
