@echo off
::echo Updating SVN Files
::svn update
if exist db.sqlite3 (
	echo Removing old database (saved as db.sqlite3.old)
	if exist db.sqlite3 (
		del db.sqlite3.*
	)
	ren db.sqlite3 db.sqlite3.old
)
echo Remaking database
@echo | CALL Migrate.bat
python manage.py create_defaults
CALL StartServer.bat
echo Done
pause

