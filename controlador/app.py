from flask import Flask,render_template, request, flash,redirect, url_for
from flask_bootstrap import Bootstrap
from modelo.DAO import db, Usuarios, Estudiantes, Profesores, Grupos, Inscripciones, Materias
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
@login_required
def administrativosListado():
    u = Usuarios()
    usuarios = u.consultaGeneral()
    return render_template('administrativos/administrativosListado.html', usuarios = usuarios)


@app.route('/administrativosNuevo')
@login_required
def administrativosNuevo():
    return render_template('administrativos/administrativoNuevo.html')

@app.route('/administrativosEditar/<int:id>')
@login_required
def administrativosEditar(id):
    u=Usuarios()
    return render_template('administrativos/administrativoEditar.html', usuario=u.consultaIndividual(id))

@app.route('/administrativosEliminar/<int:id>')
@login_required
def administrativosEliminar(id):
    u = Usuarios()
    u.eliminar(id)
    flash ('Usuario eliminado con éxito!!')
    return redirect(url_for('administrativosListado'))

@app.route('/administrativosDatosNuevo',methods=['post'])
@login_required
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
@login_required
def consultarImagenUsuario(id):
    u = Usuarios()
    return u.consultaIndividual(id).foto

@app.route('/administrativosDatosEdicion',methods=['post'])
@login_required
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
@login_required
def administrativoPerfil():
    return render_template('administrativos/administrativoEditar.html')
###################################################################################
@app.route('/estudiantes')
@login_required
def estudiantesListado():
    u = Usuarios()
    e = Estudiantes()
    usuarios=u.consultaGeneral()
    estudiantes = e.consultaGeneral()
    ul = 0;
    for id in usuarios:
        ul= id.idUsuario
    return render_template('estudiantes/estudiantesListado.html', usuarios=usuarios, estudiantes = estudiantes,ul=ul)

@app.route('/estudiantesNuevo/<int:id>')
@login_required
def estudiantesNuevo(id):
    u = Usuarios()
    usuario = u.consultaIndividual(id)
    return render_template('estudiantes/estudianteNuevo.html',usuario=usuario)

@app.route('/estudiantesEditar/<int:id>')
@login_required
def estudiantesEditar(id):
    u = Usuarios()
    e = Estudiantes()
    return render_template('estudiantes/estudianteEditar.html',usuario=u.consultaIndividual(id),estudiante=e.consultaGeneral())

@app.route('/estudianteEliminar/<int:id>')
@login_required
def estudiantesEliminar(id):
    u = Usuarios()
    e= Estudiantes()
    estudiantes = e.consultaGeneral()
    for idUs in estudiantes:
        if idUs.idUsuario == id:
            print(idUs.noControl)
            e.eliminar(idUs.noControl)
    u.eliminar(id)
    flash ('Estudiante eliminado con éxito!!')
    return redirect(url_for('estudiantesListado'))

@app.route('/estudiantesDatosNuevo',methods=['post'])
@login_required
def estudiantesDatosNuevo():
    e = Estudiantes()
    u= Usuarios()
    u.idUsuario= 1 + int(request.form['idUsuario'])
    u.foto=request.files['foto'].read()
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.domicilio=request.form['domicilio']
    u.tipo= 'E'
    u.email=request.form['email']
    u.clave=request.form['clave']
    u.insertar()
    e.noControl=request.form['noControl']
    e.idUsuario= 1 + int(request.form['idUsuario'])
    e.fechaNacimiento=request.form['fechaNacimiento']
    e.fechaIngreso=request.form['fechaIngreso']
    e.insertar()
    flash('Se ha registrado un nuevo estudiante con éxito!!')
    return redirect(url_for('estudiantesListado'))

@app.route('/estudiantesDatosEdicion',methods=['post'])
@login_required
def estudiantesDatosEdicion():
    e = Estudiantes()
    u= Usuarios()
    u.idUsuario=request.form['idUsuario']
    imagen=request.files['foto'].read()
    if imagen:
        u.foto=imagen
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.domicilio=request.form['domicilio']
    u.tipo= 'E'
    u.email=request.form['email']
    u.clave=request.form['clave']
    estatus=request.values.get('estatus',False)
    if estatus=="True":
        u.estatus=True
    else:
        u.estatus=False
    u.actualizar()
    e.noControl=request.form['noControl']
    e.idUsuario= request.form['idUsuario']
    e.fechaNacimiento=request.form['fechaNacimiento']
    e.fechaIngreso=request.form['fechaIngreso']
    e.promedioGeneral=request.form['promedioGeneral']
    e.actualizar()
    flash('Se han guardado los cambios con éxito!!')
    return render_template('estudiantes/estudianteEditar.html',usuario=u.consultaIndividual(request.form['idUsuario']),estudiante=e.consultaGeneral())

###################################################################################
@app.route('/profesores')
@login_required
def profesoresListado():
    u = Usuarios()
    p = Profesores()
    usuarios=u.consultaGeneral()
    profesores = p.consultaGeneral()
    ul = 0;
    for id in usuarios:
        ul= id.idUsuario
    return render_template('profesores/profesoresListado.html', usuarios=usuarios, profesores = profesores,ul=ul)

@app.route('/profesoresNuevo/<int:id>')
@login_required
def profesoresNuevo(id):
    u = Usuarios()
    usuario = u.consultaIndividual(id)
    return render_template('profesores/profesorNuevo.html', usuario = usuario)

@app.route('/profesoresEditar/<int:id>')
@login_required
def profesoresEditar(id):
    u = Usuarios()
    p = Profesores()
    return render_template('profesores/profesorEditar.html',usuario=u.consultaIndividual(id),profesor=p.consultaGeneral())

@app.route('/profesorEliminar/<int:id>')
@login_required
def profesoresEliminar(id):
    u = Usuarios()
    p= Profesores()
    profesores = p.consultaGeneral()
    for idUs in profesores:
        if idUs.idUsuario == id:
            p.eliminar(idUs.idProfesor)
    u.eliminar(id)
    flash ('Profesor eliminado con éxito!!')
    return redirect(url_for('profesoresListado'))

@app.route('/profesoresDatosNuevo',methods=['post'])
@login_required
def profesoresDatosNuevo():
    u= Usuarios()
    p = Profesores()
    u.idUsuario= 1 + int(request.form['idUsuario'])
    u.foto=request.files['foto'].read()
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.domicilio=request.form['domicilio']
    u.tipo= 'P'
    u.email=request.form['email']
    u.clave=request.form['clave']
    u.insertar()
    p.especialidad=request.form['especialidad']
    p.fechaContratacion=request.form['fechaContratacion']
    p.idUsuario= 1 + int(request.form['idUsuario'])
    p.cedula=request.form['cedula']
    p.insertar()
    flash('Se ha registrado un nuevo estudiante con éxito!!')
    return redirect(url_for('profesoresListado'))


@app.route('/profesoresDatosEdicion',methods=['post'])
@login_required
def profesoresDatosEdicion():
    p = Profesores()
    u= Usuarios()
    u.idUsuario=request.form['idUsuario']
    imagen=request.files['foto'].read()
    if imagen:
        u.foto=imagen
    u.nombre=request.form['nombre']
    u.sexo=request.form['sexo']
    u.telefono=request.form['telefono']
    u.domicilio=request.form['domicilio']
    u.tipo= 'P'
    u.email=request.form['email']
    u.clave=request.form['clave']
    estatus=request.values.get('estatus',False)
    if estatus=="True":
        u.estatus=True
    else:
        u.estatus=False
    u.actualizar()
    p.idProfesor=request.form['idProfesor']
    p.especialidad=request.form['especialidad']
    p.fechaContratacion=request.form['fechaContratacion']
    p.idUsuario=request.form['idUsuario']
    p.cedula=request.form['cedula']
    p.actualizar()
    flash('Se han guardado los cambios con éxito!!')
    return render_template('profesores/profesorEditar.html',usuario=u.consultaIndividual(u.idUsuario),profesor=p.consultaGeneral())
###################################################################################
@app.route('/calificacionesEncurso')
@login_required
def calificacionesEncurso():
    return render_template('calificaciones/calificacionesEstudiante.html')

@app.route('/calificacionesKardex')
@login_required
def calificacionesKardex():
    return render_template('calificaciones/kardex.html')
###################################################################################
@app.route('/materiasImpartidas')
@login_required
def materiasImpartidas():
    return render_template('materias/materiasImpartidas.html')
###################################################################################
@app.route('/gruposListado')
@login_required
def gruposListado():
    g = Grupos()
    grup = g.consultaGeneral()
    return render_template('grupos/gruposListado.html', grupos=grup)

@app.route('/grupoNuevo')
@login_required
def gruposNuevo():
    return render_template('grupos/nuevoGrupo.html')

@app.route('/registrarGrupo',methods=['post'])
@login_required
def registrarGrupo():
    g = Grupos()
    g.nombre=request.form['nombre']
    g.grado=request.form['grado']
    g.capacidad=request.form['capacidad']
    g.insertar()
    flash('Se ha registrado un nuevo grupo con éxito!!')
    return render_template('grupos/nuevoGrupo.html')

@app.route('/gruposEditar/<int:id>')
@login_required
def gruposEditar(id):
    g= Grupos()
    return render_template('grupos/grupoEditar.html', grupo = g.consultaIndividual(id))

@app.route('/gruposEliminar/<int:id>')
@login_required
def gruposEliminar(id):
    g= Grupos()
    g.eliminar(id)
    grup = g.consultaGeneral()
    flash('Se ha eliminado el grupo con éxito!!')
    return render_template('grupos/gruposListado.html', grupos=grup)

@app.route('/gruposObtenerDatos',methods=['post'])
@login_required
def gruposObtenerDatos():
    g= Grupos()
    g.idGrupo=request.form['idGrupo']
    g.nombre=request.form['nombre']
    g.grado=request.form['grado']
    g.capacidad=request.form['capacidad']
    g.actualizar()
    flash('Se han gruardado los cambios con éxito!!')
    return render_template('grupos/grupoEditar.html', grupo = g.consultaIndividual(request.form['idGrupo']))

@app.route('/grupoCalificaciones')
@login_required
def grupoCalificaciones():
    return render_template('grupos/grupoCalificaciones.html')
###################################################################################
@app.route('/horarios')
@login_required
def horarios():
    return render_template('horarios/horarios.html')
@app.route('/generarHorario',methods=['post'])
@login_required
def horarioGenerar():
    return 'GESTIÓN DE HORARIOS'
###################################################################################
@app.route('/registroCalificaciones',methods=['post'])
@login_required
def registroCalificaciones():
    return 'SE HAN REGISTRADO LAS CALIFICACIONES'
###################################################################################
@app.route('/inscripciones')
@login_required
def inscripciones():
    g = Grupos()
    grup = g.consultaGeneral()
    return render_template('inscripciones/inscripciones.html', grupos=grup)
@app.route('/registrarInscripcion', methods=['post'])
@login_required
def registrarInscripcion():
    ins = Inscripciones()
    ins.noControl = request.form['noControl']
    ins.idGrupo = request.form['idGrupo']
    ins.idCiclo = 4
    ins.insertar()
    flash('Se ha registrado la inscripción con éxito!!')
    return render_template('inscripciones/inscripciones.html')
#################################################################################
@app.route('/materiasListado')
@login_required
def materiasListado():
    m = Materias()
    mat = m.consultaGeneral()
    return render_template('materias/materiasListado.html', materias=mat)

@app.route('/materiaNuevo')
@login_required
def materiaNuevo():
    return render_template('materias/nuevaMateria.html')

@app.route('/registrarMateria',methods=['post'])
@login_required
def registrarMateria():
    m = Materias ()
    m.nombre=request.form['nombre']
    m.grado=request.form['grado']
    m.insertar()
    flash('Se ha registrado una nueva materia con éxito!!')
    return render_template('materias/nuevaMateria.html')

@app.route('/materiasEditar/<int:id>')
@login_required
def materiasEditar(id):
    m= Materias()
    return render_template('materias/materiaEditar.html', materia = m.consultaIndividual(id))

@app.route('/materiasEliminar/<int:id>')
@login_required
def materiasEliminar(id):
    m= Materias()
    m.eliminar(id)
    mat = m.consultaGeneral()
    flash('Se ha eliminado la materia con éxito!!')
    return render_template('materias/materiasListado.html', materias=mat)

@app.route('/materiasObtenerDatos',methods=['post'])
@login_required
def materiasObtenerDatos():
    m= Materias()
    m.idMateria=request.form['idMateria']
    m.nombre=request.form['nombre']
    m.grado=request.form['grado']
    m.actualizar()
    flash('Se han gruardado los cambios con éxito!!')
    return render_template('materias/materiaEditar.html', materia = m.consultaIndividual(request.form['idMateria']))

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)

