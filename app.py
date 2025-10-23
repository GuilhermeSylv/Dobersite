from flask import Flask, session, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///usuarios.db"
# ^ define onde fica a database e cria um arquiv local (usuarios.db) ^
db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    email = db.Column(db.String(300), nullable=False, primary_key=True)
    nome = db.Column(db.String(200), unique=False, nullable = False)
    senha = db.Column(db.String(100), unique=False, nullable=False)
    # ^ define a tabela, colunas, etc ^
    def __repr__(self):
        return f"<Usuario {self.email}>"
    # ^ método repr serve para retornar exatamente o mesmo valor enviado ao console, no código, etc ^
    # ^ self é uma referência ao objeto manipulado (Usuario) ^ 
app.secret_key = 'segredo'

@app.route('/')
def home():
    if session.get('logado'):
        usuario = session.get('usuario')
        return render_template('home.html', usuario=usuario)
    return redirect('/login')

@app.route('/login')
def login():
    if session.get('logado'):
        return redirect('/')
    return render_template('login.html')

@app.route('/autenticar', methods=['POST'])
def autenticar():
    login = request.form.get('login')
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    tipologin = request.form.get('logcad')

    msg_erro_cadastro = "Já existe um usuário cadastrado com este login."
    msg_erro_login = "Login e/ou senha inválidos."
    msg = ""

    if tipologin == 'Logar':
        usuario = Usuario.query.filter_by(email=login, nome=nome, senha=senha).first()
        if usuario:
            session['logado'] = True
            session['usuario'] = usuario.email
            return redirect('/')
        else:
            msg = msg_erro_login
            return render_template('login.html', msg=msg)
    
    elif tipologin == 'Cadastrar':
        existente = Usuario.query.filter_by(email=login).first()
        # ^ método Query serve especificamente para banco de dados. Passa uma instrução/consulta (aqui, filter_by, que filtra por um parâmetro X) ^
        # ^ first() retorna o primeiro objeto a seguir com os parâmetros ^
        if existente:
            msg = msg_erro_cadastro
            return render_template('login.html', msg=msg)

    novo = Usuario(email=login, nome=nome, senha=senha)
    db.session.add(novo)
    db.session.commit()

    # ^ Operações CRUD básicas (adicionar e confirmas) 

    msg = "Usuário cadastrado com sucesso! Faça login."
    return render_template('login.html', msg=msg)


@app.route('/sair')
def sair():
    if not session.get('logado'):
        return redirect('/login')
    return render_template('logsair.html')

@app.route('/confirmar', methods=['POST'])
def confirmar():
    escolha = request.form.get('escolha')

    if escolha == 'Sim':
        session.clear()
        return redirect('/login')
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        usuarios = Usuario.query.all()
        print(usuarios)
    app.run(debug=True)