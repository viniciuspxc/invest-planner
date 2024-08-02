# invest-planner
Projeto de Simulador de Investimentos

# Instalação local
python -m venv env   
.\env\Scripts\activate

# requirements.txt
pip install -r requirements.txt

# executar Django
python .\invest_planner\manage.py makemigrations
python .\invest_planner\manage.py migrate          
python .\invest_planner\manage.py runserver          

# pylint Command:
pylint --load-plugins pylint_django --django-settings-module=invest_planner.settings .\invest_planner\invest_planner\ .\invest_planner\base\ .\invest_planner\login_app\
