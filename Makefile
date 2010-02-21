# Makefile for the google appengine application

# help is found here: <http://code.google.com/appengine/docs/python/gettingstarted/>


# ---- clean the directory from unneeded files
.PHONY : clean
clean :
	-rm -rf *~ *.pyc

# ---- upload your code to google appengine:
deploy:
	~/Downloads/google_appengine/appcfg.py update ./

