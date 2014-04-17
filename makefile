.PHONY: install remove_media remove_pyc update_virtualenv remove_db create_db load_fixtures geoip

localsite: install 

install: clean update_virtualenv 

clean: remove_pyc

remove_pyc:
	-find . -type f -name "*.pyc" -delete

update_virtualenv:
	pip install -r www/deploy/requirements.txt

remove_db:
	python www/manage.py reset_db --router=default --noinput

create_db:
	python www/manage.py syncdb --noinput --traceback
	python www/manage.py migrate --traceback

load_fixtures:
	python www/manage.py loaddata fixtures/*
