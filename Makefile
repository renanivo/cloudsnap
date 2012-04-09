A=/usr/local/google_appengine
setup:
	@pip install -r requirements.txt
	@cp cloudsnap/settings.example.py cloudsnap/settings.py
	@if [ ! -d "$A" ]; then echo "Warning: App Engine SDK not found."; fi;
test:
	nosetests --with-gae --without-sandbox --gae-lib-root $A --gae-application cloudsnap
