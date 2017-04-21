#echo Updating SVN Files
#svn update
if [ ! -f db.sqlite3]; then
	echo "Removing old database (saved as db.sqlite3.old)"
	rm db.sqlite3.*
	mv db.sqlite3 db.sqlite3.old
fi
echo "Removing old migrations (moved to migrations_old)"
for dir in *; do
	if [ ! -d "$dir\migrations"]; then
		if [ ! -d "$dir\migrations_old"]; then
			rm -rf "$dir\migrations_old"
		fi
		mv "$dir\migrations" "migrations_old"
		mkdir "$dir\migrations"
		touch "$dir\migrations\__init__.py"
	fi
done
echo "Remaking database"
python manage.py makemigrations
python manage.py migrate
python manage.py create_defaults
python manage.py runserver
echo "Done"
sleep 3s