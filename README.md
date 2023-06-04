# CoinStash
A cryptocurrency portfolio manager.

Landing page:


https://github.com/dfloren/CoinStash-public/assets/43223710/3f1b0189-b773-4dae-ae1c-5e9efb9af7de

Chart demo:


https://user-images.githubusercontent.com/43223710/164985408-48365fb0-3761-4004-a826-d2a49c13551b.mp4

Transactions demo:


https://user-images.githubusercontent.com/43223710/164985414-e318ab6e-b9d1-4f7b-8cdb-cdc2cf2d2713.mp4


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
