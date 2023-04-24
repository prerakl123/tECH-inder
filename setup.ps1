python -m pip install --upgrade pip
pip install virtualenv
virtualenv venv

Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
.\venv\Scripts\activate
pip install -r requirements.txt
flask db init
flask db migrate
flask db upgrade
flask run