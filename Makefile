GAE_ROOT=/usr/local/google_appengine
setup:
	@pip install -r requirements.txt
	@cp cloudsnap/settings.example.py cloudsnap/settings.py
	@if [ ! -d "$(GAE_ROOT)" ]; then echo "Warning: App Engine SDK not found."; fi;
test:
	nosetests --with-gae --without-sandbox --gae-lib-root $(GAE_ROOT) --gae-application cloudsnap
