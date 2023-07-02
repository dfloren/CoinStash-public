# CoinStash
A cryptocurrency portfolio manager.

Landing page:


https://github.com/dfloren/CoinStash-public/assets/43223710/3f1b0189-b773-4dae-ae1c-5e9efb9af7de

Features:


https://github.com/dfloren/CoinStash-public/assets/43223710/fdcc691a-a314-4060-afb1-7eb1b6769e9f


## Running locally
Follow these steps to run the app on local:
1. Install the python modules. It is recommended to create and activate a virtual environment first.
```terminal
(venv) > pip install -r requirements.txt
```
2. Collect static files.
```terminal
(venv) > python manage.py collectstatic
```
3. Create a PostgreSQL database with credentials specified in `ProjCryptoCurrency/settings.py`. The default credentials are `daniel`/`daniel`.
4. Run the database migrations.
```terminal
(venv) > python manage.py migrate
```
5. Populate coin list. This step requires an internet connection and may take a few minutes to finish.
```terminal
(venv) > python manage.py shell
(venv) > from AppCoinStash.coin_api import update_coin_list
(venv) > update_coin_list()
```
6. Run the app and open http://127.0.0.1:8000 
```terminal
(venv) > python manage.py runserver
```
