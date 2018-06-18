#!/bin/sh

cd /home/happyschool/happyschool/Script #Chemin vers le script

yes |python3 manage.py makemigrations annuaire
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations absence_prof
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations admin
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations appels
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations auth
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations authtoken
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations contenttypes
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations core
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations dossier_eleve
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations infirmerie
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations mail_answer
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations mail_notification
yes |python3 manage.py migrate

yes |python3 manage.py makemigrations sessions
yes |python3 manage.py migrate



