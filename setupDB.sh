#!/bin/bash
#This is to be used only for the occassion
# that the first time the database gets installed

export FLASK_APP=bookworm
env=( development staging production default )

# Create our first time DBase creation
flask db init

# create our databases
for elem in "${env[@]}"
do
	export APP_CONFIG_FILE="../config/$elem.py"
  flask db migrate
  flask db upgrade
	python provisionDB.py
done
