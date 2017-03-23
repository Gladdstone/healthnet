@echo off
echo Updating SVN Files
svn update
if exist db.sqlite3 (
	echo Removing old database (saved as db.sqlite3.old)
	if exist db.sqlite3 (
		rm db.sqlite3.old
	)
	ren db.sqlite3 db.sqlite3.old
)
for /D %%f in (*) do (
	if exist "%%f\migrations" (
		if exist "%%f\migrations_old" (
			rmdir /Q /S "%%f\migrations_old"
		)
		rename "%%f\migrations" "migrations_old"
	)
)
start cmd /k python manage.py runserver
python manage.py makemigrations
python manage.py migrate
echo Done
pause

