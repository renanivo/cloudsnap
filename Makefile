GAE_ROOT=/usr/local/google_appengine
setup:
	@pip install -r requirements_dev.txt
	@pip install --install-option="--install-purelib=$(shell pwd)/cloudsnap" -r requirements.txt
	@cp cloudsnap/settings.example.py cloudsnap/settings.py
	@if [ ! -d "$(GAE_ROOT)" ]; then echo "Warning: App Engine SDK not found."; fi;
test:
	nosetests --with-gae --without-sandbox --gae-lib-root $(GAE_ROOT) --gae-application cloudsnap
coverage-report:
	nosetests --with-coverage --cover-html --cover-erase --with-gae --without-sandbox --gae-lib-root $(GAE_ROOT) --gae-application cloudsnap
deploy:
	appcfg.py update cloudsnap
