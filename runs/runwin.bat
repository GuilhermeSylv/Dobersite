@REM ^ Rode esse arquivo para abrir o ambiente virtual sem precisar do terminal ^

@echo off
@REM ^ Echo off serve pra manter o terminal limpo ^
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
@REM ^ Instala as requisições (bibliotecas) para o código funcionar ^
echo Ambiente pronto.

set FLASK_APP=app.py
set FLASK_ENV=development
@REM ^ Variáveis do próprio Flask: FLASK_APP é app.py, ou seja, o aplicativo principal ^
@REM ^ FLASK_ENV define o contexto e o ambiente em que o Flask vai ser executado. Aqui, modo de desenvolvimento para possibilitar o debug, entre outros ^

echo Iniciando servidor Flask e abrindo navegador...
start "" runs\venv\Scripts\python.exe -m flask run
timeout /t 10
start http://127.0.0.1:5000

pause
