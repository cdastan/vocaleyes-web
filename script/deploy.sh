#!/bin/bash

ROOT_DIR=/apps/localeyes
SSH_COMMAND="ssh localeyes"
#ANALYTICS="<script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)})(window,document,'script','//www.google-analytics.com/analytics.js','ga'); ga('create', 'UA-36430066-7', 'wuery.com'); ga('send', 'pageview');</script>"

# * Remove debug flag. * Add analytics
# sed is different on OS X
if [[ $(uname) == "Darwin" ]]; then
    sed -i '' "s/debug = True/debug = False/" app/config.py
    # sed -i '' "s#<\!--analytics-->#$ANALYTICS#" app/www/templates/base.html # ! is escaped
else
    sed -i "s/debug = True/debug = False/" app/config.py
    # sed -i "s#<\!--analytics-->#$ANALYTICS#" app/www/templates/base.html  # ! is escaped
fi


# DEPLOY
# ------
echo "Deploying project ..."
# rsync:
# -a archive (a shortcut for a bunch of commands actually)
# -v verbose, -z compress when transferring
rsync -avzh ./ -e $SSH_COMMAND:$ROOT_DIR --exclude .git --exclude .DS_Store --exclude .gitignore --exclude venv* --exclude var
$SSH_COMMAND circusctl reload
echo "Deploy done."


# REVER BUILD CHANGES
# ------------------
git checkout .
