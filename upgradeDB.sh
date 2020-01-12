#!/bin/bash
#This is to be used when the database structure changes

#N.B. SQLite doesn't support alter table so you have to kludge it
#with the following fragment/example
#    with op.batch_alter_table('books') as batch_op:
#        batch_op.drop_column('food')
export FLASK_APP=bookworm
env=( development staging production default)


# Update our database structure for all environments
for elem in "${env[@]}"
do
	export APP_CONFIG_FILE="../config/$elem.py"
  flask db migrate
  flask db upgrade
	python provisionDB.py
done
