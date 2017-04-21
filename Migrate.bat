@echo off
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
python manage.py makemigrations
python manage.py migrate
pause