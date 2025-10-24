@echo off
cd ..
IF NOT EXIST "runs\venv" (
    echo Criando ambiente...
    python -m venv runs\venv
) ELSE (
    echo Ambiente já existe.
)

call runs\venv\Scripts\activate
@REM ^ Call chama um script externo no bat ^
python -m pip install -r requisicoes\bibliotecas.txt

echo Ambiente pronto.

set FLASK_APP=app.py
set FLASK_ENV=development

echo Iniciando servidor Flask e abrindo navegador...
start "" runs\venv\Scripts\python.exe -m flask run
timeout /t 10
start http://127.0.0.1:5000

pause