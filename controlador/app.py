from flask import Flask,render_template, request, flash,redirect, url_for
from flask_bootstrap import Bootstrap
from modelo.DAO import db, Usuarios, Estudiantes, Profesores, Grupos
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

app = Flask(__name__, template_folder='../vista',static_folder='../static')
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://userCalifSecVillaRosa:Hola.123@localhost/CalifSecVillaRosa'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='cl4v3'
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.login_message = u"Debes iniciar sesión !"

@login_manager.user_loader
def load_user(id):
    return Usuarios.query.get(int(id))

@app.route('/')
def login():
    if current_user.is_authenticated:
        return render_template('comunes/index.html')
    else:
        return render_template('comunes/login.html')

@app.route('/recopilarDatosLogin',methods=['post'])
def validarUsuario():
    user=Usuarios()
    email = request.form['email']
    contraseña= request.form['password']
    user = user.validar(email, contraseña)
    if user != None:
        login_user(user)
        return render_template('comunes/index.html')
    else:
        flash('¡ Datos incorrectos !')
        return render_template('comunes/login.html')

@app.route('/cerrarSesion')
@login_required
def cerrarSesion():
    logout_user()
    return redirect(url_for('login'))

@app.route('/Index')
@login_required #DECORADOR PARA EXIGIR INICIO DE SESIÓN
def index():
    return render_template('comunes/index.html')

###################################################################################
@app.route('/administrativos')
def administrativosListado():
    u = Usuarios()
    usuarios = u.consultaGeneral()
    return render_template('administrativos/administrativosListado.html', usuarios = usuarios)

@app.route('/administrativosNuevo')
def administrativosNuevo():
    return render_template('administrativos/administrativoNuevo.html')

@app.route('/administrativosEditar/<int:id>')
def administrativosEditar(id):
    u=Usuarios()
    return render_template('administrativos/administrativoEditar.html', usuario=u.consultaIndividual(id))

@app.route('/administrativosEliminar/<int:id>')
def administrativosEliminar(id):
    u = Usuarios()
    u.eliminar(id)
    flash ('Usuario eliminado con éxito!!')
    return redirect(url_for('administrativosListado'))

@app.route('/administrativosDatosNuevo',methods=['post'])
def administrativosDatosNuevo():
    u= Usuarios()
    u.foto=request.files['foto'].read()
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.domicilio=request.form['domicilio']
    u.tipo=request.form['tipo']
    u.email=request.form['email']
    u.clave=request.form['clave']
    u.insertar()
    flash('Se ha registrado un nuevo usuario con éxito!!')
    return render_template('administrativos/administrativoNuevo.html')

@app.route('/usuarios/imagen/<int:id>')
def consultarImagenUsuario(id):
    u = Usuarios()
    return u.consultaIndividual(id).foto

@app.route('/administrativosDatosEdicion',methods=['post'])
def administrativosDatosEdicion():
    u = Usuarios()
    u.idUsuario=request.form['idUsuario']
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.domicilio=request.form['domicilio']
    u.tipo=request.form['tipo']
    u.email=request.form['email']
    u.clave=request.form['clave']
    estatus=request.values.get('estatus',False)
    if estatus=="True":
        u.estatus=True
    else:
        u.estatus=False
    imagen=request.files['foto'].read()
    if imagen:
        u.foto=imagen
    u.actualizar()
    flash('Usuario editado con éxito!!')
    return render_template('administrativos/administrativoEditar.html',usuario=u)

@app.route('/administrativoPerfil')
def administrativoPerfil():
    return render_template('administrativos/administrativoEditar.html')
###################################################################################
@app.route('/estudiantes')
def estudiantesListado():
    u = Usuarios()
    e = Estudiantes()
    usuarios=u.consultaGeneral()
    estudiantes = e.consultaGeneral()
    return render_template('estudiantes/estudiantesListado.html', usuarios=usuarios, estudiantes = estudiantes)

@app.route('/estudiantesNuevo')
def estudiantesNuevo():
    return render_template('estudiantes/estudianteNuevo.html')

@app.route('/estudiantesEditar')
def estudiantesEditar():
    return render_template('estudiantes/estudianteEditar.html')

@app.route('/estudiantesEliminar')
def estudiantesEliminar():
    return 'SE HA ELIMINADO UN ESTUDIANTE'

@app.route('/estudiantesDatosNuevo',methods=['post'])
def estudiantesDatosNuevo():
    return 'SE HA REGISTRADO UN NUEVO ESTUDIANTE'

@app.route('/estudiantesDatosEdicion',methods=['post'])
def estudiantesDatosEdicion():
    return 'SE HAN GUARDADO LOS CAMBIOS'
###################################################################################
@app.route('/profesores')
def profesoresListado():
    u = Usuarios()
    p = Profesores()
    usuarios=u.consultaGeneral()
    profesores = p.consultaGeneral()
    return render_template('profesores/profesoresListado.html', usuarios=usuarios, profesores=profesores)

@app.route('/profesoresNuevo')
def profesoresNuevo():
    return render_template('profesores/profesorNuevo.html')

@app.route('/profesoresEditar')
def profesoresEditar():
    return render_template('profesores/profesorEditar.html')

@app.route('/profesoresEliminar')
def profesoresEliminar():
    return 'SE HA ELIMINADO UN PROFESOR'

@app.route('/profesoresDatosNuevo',methods=['post'])
def profesoresDatosNuevo():
    return 'SE HA REGISTRADO UN NUEVO PROFESOR'

@app.route('/profesoresDatosEdicion',methods=['post'])
def profesoresDatosEdicion():
    return 'SE HAN GUARDADO LOS CAMBIOS'
###################################################################################
@app.route('/calificacionesEncurso')
def calificacionesEncurso():
    return render_template('calificaciones/calificacionesEstudiante.html')

@app.route('/calificacionesKardex')
def calificacionesKardex():
    return render_template('calificaciones/kardex.html')
###################################################################################
@app.route('/materiasImpartidas')
def materiasImpartidas():
    return render_template('materias/materiasImpartidas.html')
###################################################################################
@app.route('/gruposListado')
def gruposListado():
    g = Grupos()
    grup = g.consultaGeneral()
    return render_template('grupos/gruposListado.html', grupos=grup)


@app.route('/grupoCalificaciones')
def grupoCalificaciones():
    return render_template('grupos/grupoCalificaciones.html')
###################################################################################
@app.route('/horarios')
def horarios():
    return render_template('horarios/horarios.html')
@app.route('/generarHorario',methods=['post'])
def horarioGenerar():
    return 'GESTIÓN DE HORARIOS'
###################################################################################
@app.route('/registroCalificaciones',methods=['post'])
def registroCalificaciones():
    return 'SE HAN REGISTRADO LAS CALIFICACIONES'
###################################################################################
@app.route('/inscripciones')
def inscripciones():
    return render_template('inscripciones/inscripciones.html')

@app.route('/registrarInscripcion', methods=['post'])
def registrarInscripcion():
    return 'SE HA REALIZADO UNA INSCRIPCIÓN'


if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)