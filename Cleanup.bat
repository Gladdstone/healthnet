@echo off
::echo Updating SVN Files
::svn update
if exist db.sqlite3 (
	echo Removing old database (saved as db.sqlite3.old)
	if exist db.sqlite3 (
		del db.sqlite3.old
	)
	ren db.sqlite3 db.sqlite3.old
)
echo Removing old migrations (moved to migrations_old)
for /D %%f in (*) do (
	if exist "%%f\migrations" (
		if exist "%%f\migrations_old" (
			rmdir /Q /S "%%f\migrations_old"
		)
		rename "%%f\migrations" "migrations_old"
		mkdir "%%f\migrations"
		copy NUL "%%f\migrations\__init__.py"
	)
)
echo Remaking database
python manage.py makemigrations
python manage.py migrate
python manage.py create_defaults
StartServer.bat
echo Done
pause

