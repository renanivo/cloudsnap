A=/opt/google_appengine
setup:
	@add2virtualenv cloudsnap
	@pip install -r requirements.txt
	@if [ ! -d "$A" ]; then echo "Warning: App Engine SDK not found."; fi;
test:
	nosetests --with-gae --without-sandbox --gae-lib-root $A --gae-application cloudsnap
