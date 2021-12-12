from flask import Flask,render_template, request, flash,redirect, url_for,abort
from flask_bootstrap import Bootstrap
from modelo.DAO import db, Usuarios, Estudiantes, Profesores, Grupos, Inscripciones, Materias, cicloEscolar, Horarios,Calificaciones, DetalleCalificaciones
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

app = Flask(__name__, template_folder='../vista',static_folder='../static')
Bootstrap(app)
import json
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
    if current_user.is_authenticated and current_user.is_administrador():
        u = Usuarios()
        usuarios = u.consultaGeneral()
        return render_template('administrativos/administrativosListado.html', usuarios = usuarios)
    else:
        abort(404)


@app.route('/administrativosNuevo')
@login_required

def administrativosNuevo():
      if current_user.is_authenticated and current_user.is_administrador():
            return render_template('administrativos/administrativoNuevo.html')
      else:
          abort(404)

@app.route('/administrativosEditar/<int:id>')
@login_required
def administrativosEditar(id):
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        if current_user.is_administrador():
            u=Usuarios()
            return render_template('administrativos/administrativoEditar.html', usuario=u.consultaIndividual(id))
        else:
            if current_user.is_staff() and (current_user.idUsuario==id):
                u=Usuarios()
                return render_template('administrativos/administrativoEditar.html', usuario=u.consultaIndividual(id))
            else:
                abort(404)
    else:
        abort(404)

@app.route('/administrativosEliminar/<int:id>')
@login_required
def administrativosEliminar(id):
    if current_user.is_authenticated and current_user.is_administrador():
        u = Usuarios()
        u.eliminar(id)
        flash ('Usuario eliminado con éxito!!')
        return redirect(url_for('administrativosListado'))
    else:
        abort(404)


@app.route('/administrativosDatosNuevo',methods=['post'])
@login_required
def administrativosDatosNuevo():
    if current_user.is_authenticated and current_user.is_administrador():
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
    else:
        abort(404)

@app.route('/usuarios/imagen/<int:id>')
@login_required
def consultarImagenUsuario(id):

        u = Usuarios()
        return u.consultaIndividual(id).foto

@app.route('/administrativosDatosEdicion',methods=['post'])
@login_required
def administrativosDatosEdicion():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
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
    else:
        abort(404)

###################################################################################
@app.route('/estudiantes')
@login_required
def estudiantesListado():
    if current_user.is_authenticated and current_user.is_administrador():
        u = Usuarios()
        e = Estudiantes()
        usuarios=u.consultaGeneral()
        estudiantes = e.consultaGeneral()
        ul = 0;
        for id in usuarios:
            ul= id.idUsuario
        return render_template('estudiantes/estudiantesListado.html', usuarios=usuarios, estudiantes = estudiantes,ul=ul)
    else:
        abort(404)

@app.route('/estudiantesNuevo/<int:id>')
@login_required
def estudiantesNuevo(id):
    if current_user.is_authenticated and current_user.is_administrador():
        u = Usuarios()
        usuario = u.consultaIndividual(id)
        return render_template('estudiantes/estudianteNuevo.html',usuario=usuario)
    else:
        abort(404)

@app.route('/estudiantesEditar/<int:id>')
@login_required
def estudiantesEditar(id):
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_estudiante()):
        if current_user.is_administrador():
            u = Usuarios()
            e = Estudiantes()
            return render_template('estudiantes/estudianteEditar.html',usuario=u.consultaIndividual(id),estudiante=e.consultaGeneral())
        else:
            if current_user.is_estudiante() and (current_user.idUsuario==id):
                u = Usuarios()
                e = Estudiantes()
                return render_template('estudiantes/estudianteEditar.html',usuario=u.consultaIndividual(id),estudiante=e.consultaGeneral())
            else:
                abort(404)
    else:
        abort(404)

@app.route('/estudianteEliminar/<int:id>')
@login_required
def estudiantesEliminar(id):
    if current_user.is_authenticated and current_user.is_administrador():
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
    else:
        abort(404)

@app.route('/estudiantesDatosNuevo',methods=['post'])
@login_required
def estudiantesDatosNuevo():
    if current_user.is_authenticated and current_user.is_administrador():
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
    else:
        abort(404)

@app.route('/estudiantesDatosEdicion',methods=['post'])
@login_required
def estudiantesDatosEdicion():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_estudiante()):
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
    else:
        abort(404)

###################################################################################
@app.route('/profesores')
@login_required
def profesoresListado():
    if current_user.is_authenticated and current_user.is_administrador():
        u = Usuarios()
        p = Profesores()
        usuarios=u.consultaGeneral()
        profesores = p.consultaGeneral()
        ul = 0;
        for id in usuarios:
            ul= id.idUsuario
        return render_template('profesores/profesoresListado.html', usuarios=usuarios, profesores = profesores,ul=ul)
    else:
        abort(404)

@app.route('/profesoresNuevo/<int:id>')
@login_required
def profesoresNuevo(id):
    if current_user.is_authenticated and current_user.is_administrador():
        u = Usuarios()
        usuario = u.consultaIndividual(id)
        return render_template('profesores/profesorNuevo.html', usuario = usuario)
    else:
        abort(404)

@app.route('/profesoresEditar/<int:id>')
@login_required
def profesoresEditar(id):
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_profesor()):
        if current_user.is_administrador():
            u = Usuarios()
            p = Profesores()
            return render_template('profesores/profesorEditar.html',usuario=u.consultaIndividual(id),profesor=p.consultaGeneral())
        else:
            if current_user.is_profesor() and (current_user.idUsuario == id):
                u = Usuarios()
                p = Profesores()
                return render_template('profesores/profesorEditar.html',usuario=u.consultaIndividual(id),profesor=p.consultaGeneral())
            else:
                abort(404)
    else:
        abort(404)

@app.route('/profesorEliminar/<int:id>')
@login_required
def profesoresEliminar(id):
    if current_user.is_authenticated and current_user.is_administrador():
        u = Usuarios()
        p= Profesores()
        profesores = p.consultaGeneral()
        for idUs in profesores:
            if idUs.idUsuario == id:
                p.eliminar(idUs.idProfesor)
        u.eliminar(id)
        flash ('Profesor eliminado con éxito!!')
        return redirect(url_for('profesoresListado'))
    else:
        abort(404)

@app.route('/profesoresDatosNuevo',methods=['post'])
@login_required
def profesoresDatosNuevo():
    if current_user.is_authenticated and current_user.is_administrador():
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
    else:
        abort(404)


@app.route('/profesoresDatosEdicion',methods=['post'])
@login_required
def profesoresDatosEdicion():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_profesor()):
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
    else:
        abort(404)

@app.route('/usuarios/email/<string:email>', methods=['get'])
def consultarEmail(email):
        usuario = Usuarios()
        return json.dumps(usuario.consultarEmail(email))

@app.route('/estudiantes/noControl/<string:noControl>', methods=['get'])
def consultarnoControl(noControl):
        estudiantes = Estudiantes()
        return json.dumps(estudiantes.consultarNoCont(noControl))

@app.route('/usuarios/telefono/<string:telefono>', methods=['get'])
def consultarTelefono(telefono):
        usuario = Usuarios()
        return json.dumps(usuario.consultarTelefono(telefono))

@app.route('/usuarios/nombre/<string:nombre>', methods=['get'])
def consultarNombre(nombre):
        usuario = Usuarios()
        return json.dumps(usuario.consultarNombre(nombre))

@app.route('/grupo/nombre/<string:nombre>',methods=['get'])
def consultarGrupo(nombre):
    grupo=Grupos()
    return json.dumps(grupo.consultarGrupos(nombre))
###################################################################################
@app.route('/calificacionesEncurso')
@login_required
def calificacionesEncurso():
    if current_user.is_authenticated and current_user.is_estudiante():
        g=Grupos()
        grupos = g.consultaGeneral()
        i = Inscripciones()
        inscrip = i.consultaGeneral()
        e = Estudiantes()
        est = e.consultaGeneral()
        noControl = ''
        for es in est:
            if es.idUsuario == current_user.idUsuario:
                noControl = es.noControl
        idGrupo=0
        for ins in inscrip:
            if ins.noControl==noControl:
                idGrupo=ins.idGrupo
        c= cicloEscolar()
        idCiclo=0
        nombreciclo=''
        for cc in c.consultaGeneral():
            idCiclo = cc.idCiclo
            nombreciclo = cc.nombre

        c = Calificaciones()
        d = DetalleCalificaciones()
        calificaciones = c.consultaIndividual(noControl)
        detalle = d.consultaGeneral()
        m = Materias()
        return render_template('calificaciones/calificacionesEstudiante.html',ciclo=nombreciclo,idGrupo=idGrupo, grupos=grupos,
                               calificaciones=calificaciones, idCiclo=idCiclo, materias=m.consultaGeneral(), detalle=detalle)
    else:
        abort(404)

@app.route('/calificacionesKardex')
@login_required
def calificacionesKardex():
    if current_user.is_authenticated and current_user.is_estudiante():
        g=Grupos()
        grupos = g.consultaGeneral()
        i = Inscripciones()
        inscrip = i.consultaGeneral()
        e = Estudiantes()
        est = e.consultaGeneral()
        noControl = ''
        for es in est:
            if es.idUsuario == current_user.idUsuario:
                noControl = es.noControl
        idGrup=0
        for ins in inscrip:
            if ins.noControl==noControl:
                idGrup=ins.idGrupo

        c = Calificaciones()
        calificaciones = c.consultaIndividual(noControl)
        cicl = cicloEscolar()
        ciclos = cicl.consultaGeneral()
        m = Materias()
        materias = m.consultaGeneral()

        cicloActual=0
        for cc in ciclos:
            cicloActual = cc.idCiclo
        return render_template('calificaciones/kardex.html', grupos = grupos, inscripciones= inscrip,grupo=idGrup,
                               noControl=noControl, estudiantes=est, calificaciones= calificaciones, ciclos=ciclos,
                               materias=materias, cicloActual=cicloActual)
    else:
        abort(404)


@app.route('/calificaciones')
@login_required
def calificaciones():
    if current_user.is_authenticated and current_user.is_staff():
        g=Grupos()
        grupos = g.consultaGeneral()
        i = Inscripciones()
        inscrip = i.consultaGeneral()
        e = Estudiantes()
        est = e.consultaGeneral()
        c = Calificaciones()
        calificaciones = c.consultaGeneral()
        cicl = cicloEscolar()
        ciclos = cicl.consultaGeneral()
        m = Materias()
        materias = m.consultaGeneral()
        u = Usuarios()
        return render_template('calificaciones/calificaciones.html', grupos = grupos, inscripciones= inscrip,
                                estudiantes=est, calificaciones= calificaciones, ciclos=ciclos,
                               materias=materias, usuarios=u.consultaGeneral())
    else:
        abort(404)

@app.route('/detallecalificaciones')
@login_required
def detallecalificaciones():
    if current_user.is_authenticated and current_user.is_staff():
        g=Grupos()
        grupos = g.consultaGeneral()
        i = Inscripciones()
        inscrip = i.consultaGeneral()
        e = Estudiantes()
        est = e.consultaGeneral()
        c = Calificaciones()
        calificaciones = c.consultaGeneral()
        cicl = cicloEscolar()
        ciclos = cicl.consultaGeneral()
        m = Materias()
        materias = m.consultaGeneral()
        u = Usuarios()
        d = DetalleCalificaciones()
        detalle = d.consultaGeneral()
        return render_template('calificaciones/detalleCalificaciones.html', grupos = grupos, inscripciones= inscrip,
                               estudiantes=est, calificaciones= calificaciones, ciclos=ciclos,
                               materias=materias, usuarios=u.consultaGeneral(),detalle=detalle)
    else:
        abort(404)
###################################################################################
@app.route('/materiasImpartidas')
@login_required
def materiasImpartidas():
    if current_user.is_authenticated and current_user.is_profesor():
        m = Materias()
        p = Profesores()
        h = Horarios()
        g = Grupos()
        u = Usuarios()
        return render_template('materias/materiasImpartidas.html', materias=m.consultaGeneral(),
                               profesores=p.consultaGeneral(), horarios=h.consultaGeneral(), grupos=g.consultaGeneral(),
                               usuario=u.consultaGeneral())
    else:
            abort(404)

@app.route('/obtenerGrupo/<int:id>')
@login_required
def obtenerGrupo(id):
    if current_user.is_authenticated and current_user.is_profesor():
        m = Materias()
        mat = m.consultaGeneral()
        p = Profesores()
        h = Horarios()
        g = Grupos()
        u = Usuarios()
        nombreGrupo = 1
        nombreH = []
        grupoSi = []
        materiaSi = []
        idUs = u.consultaIndividual(id)
        hora = h.consultaGeneral()
        pr = p.consultaGeneral()
        for pi in pr:
            if pi.idUsuario == idUs.idUsuario:
                for m in mat:
                    for hh in hora:
                        if m.idMateria == hh.idMateria:
                            if hh.idProfesor == pi.idProfesor:
                                materiaSi.append(hh.idMateria)
                                grupoSi.append(hh.idGrupo)
                                nombreH.append(hh.idHorario)
                                break
        return render_template('materias/materiasImpartidas.html', materias=m.consultaGeneral(),
                               profesores=p.consultaGeneral(), horarios=h.consultaGeneral(),
                               grupos=g.consultaGeneral(),
                               usuario=u.consultaGeneral(), grupoSi=grupoSi, materiaSi=materiaSi, nombreH=nombreH)
    else:
        abort(404)

###################################################################################
@app.route('/gruposListado')
@login_required
def gruposListado():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        g = Grupos()
        grup = g.consultaGeneral()
        return render_template('grupos/gruposListado.html', grupos=grup)
    else:
        abort(404)

@app.route('/grupoNuevo')
@login_required
def gruposNuevo():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        return render_template('grupos/nuevoGrupo.html')
    else:
        abort(404)

@app.route('/registrarGrupo',methods=['post'])
@login_required
def registrarGrupo():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        g = Grupos()
        g.nombre=request.form['nombre']
        g.grado=request.form['grado']
        g.capacidad=request.form['capacidad']
        g.insertar()
        flash('Se ha registrado un nuevo grupo con éxito!!')
        return render_template('grupos/nuevoGrupo.html')
    else:
        abort(404)

@app.route('/gruposEditar/<int:id>')
@login_required
def gruposEditar(id):
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        g= Grupos()
        return render_template('grupos/grupoEditar.html', grupo = g.consultaIndividual(id))
    else:
        abort(404)

@app.route('/gruposEliminar/<int:id>')
@login_required
def gruposEliminar(id):
    if current_user.is_authenticated and current_user.is_administrador():
        g= Grupos()
        g.eliminar(id)
        grup = g.consultaGeneral()
        flash('Se ha eliminado el grupo con éxito!!')
        return render_template('grupos/gruposListado.html', grupos=grup)
    else:
        abort(404)

@app.route('/gruposObtenerDatos',methods=['post'])
@login_required
def gruposObtenerDatos():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        g= Grupos()
        g.idGrupo=request.form['idGrupo']
        g.nombre=request.form['nombre']
        g.grado=request.form['grado']
        g.capacidad=request.form['capacidad']
        g.actualizar()
        flash('Se han gruardado los cambios con éxito!!')
        return render_template('grupos/grupoEditar.html', grupo = g.consultaIndividual(request.form['idGrupo']))
    else:
        abort(404)

@app.route('/grupCalificaciones/<int:id>,<int:idh>,<string:materia>')
@login_required
def grupoCalificaciones(id,idh,materia):
    if current_user.is_authenticated and current_user.is_profesor():
        g = Grupos()
        i = Inscripciones()
        e = Estudiantes()
        u = Usuarios()
        h = Horarios()
        ci = cicloEscolar()
        c = Calificaciones()

        ciclos = ci.consultaGeneral()
        act = 0;
        for idc in ciclos:
            act = idc.idCiclo

        return render_template('grupos/grupoCalificaciones.html', grupos=g.consultaIndividual(id),
                               inscripciones=i.consultaGeneral(), estudiantes=e.consultaGeneral(),actual=act,
                               cicl=ci.consultaGeneral(),usuario=u.consultaGeneral(), horarios=h.consultaIndividual(idh), materia=materia)
    else:
        abort(404)

@app.route('/registroCalif/<int:idM>,<string:materia>,<string:estudiante>,<string:noControl>,<int:idC>,<int:idGrupo>,<int:idHorario>')
@login_required
def registroCalif(idM,materia,estudiante,noControl,idC,idGrupo,idHorario):
    if current_user.is_authenticated and current_user.is_profesor():
        c = Calificaciones()
        idCalificacion =0
        for calif in c.consultaGeneral():
            idCalificacion =calif.idCalificacion
        return render_template('calificaciones/calificacionesNuevo.html', idMateria=idM,idCiclo=idC,materia=materia,estudiante=estudiante,
                               noControl=noControl,idGrupo=idGrupo,idHorario=idHorario,idCalificacion=idCalificacion)
    else:
        abort(404)

@app.route('/grupoCalificacionesRe', methods=['post'])
@login_required
def grupoCalificacionesRegistrar():
    if current_user.is_authenticated and current_user.is_profesor():
        c = Calificaciones()
        con = c.consultaGeneral()
        existe = 0;
        idCalificacion=0;
        ciclo=0;
        for calif in con:
            if calif.idMateria == int (request.form['idMateria']) and calif.noControl == request.form['noControl']:
                existe=1;
                idCalificacion=calif.idCalificacion
                ciclo= calif.idCiclo
        if existe==1:
            d = DetalleCalificaciones()
            d.bimestre=request.form['bimestre']
            d.calificacion=request.form['calificacion']
            d.idCalificacion=idCalificacion
            d.insertar()
            c.idCalificacion=idCalificacion
            c.noControl=request.form['noControl']
            c.idMateria=request.form['idMateria']
            c.idCiclo=ciclo
            c.calificacionFinal=(calif.calificacionFinal+int(request.form['calificacion']))/2
            c.actualizar()
        else:
            c.noControl = request.form['noControl']
            c.idMateria = request.form['idMateria']
            c.idCiclo = request.form['idCiclo']
            c.calificacionFinal = request.form['calificacion']
            c.insertar()
            d = DetalleCalificaciones()
            d.bimestre=request.form['bimestre']
            d.calificacion=request.form['calificacion']
            d.idCalificacion=(1+int(request.form['idCalificacion']))
            d.insertar()
        flash('¡Se ha registrado la calificación con éxito!')
        return render_template('calificaciones/calificacionesNuevo.html', idMateria=request.form['idMateria'],idCiclo=request.form['idCiclo'],
                               materia=request.form['materia'],estudiante=request.form['nombre'],
                               noControl=request.form['noControl'],idGrupo=request.form['idGrupo'],idHorario=request.form['idHorario'],
                               idCalificacion=c.idCalificacion)
    else:
        abort(404)

@app.route('/consultaCalificaciones/<string:estudiante>,<string:noControl>,<int:idMateria>,<string:materia>,<int:idGrupo>,<int:idHorario>,<int:idCiclo>')
@login_required
def consultaCalificaciones(estudiante,noControl,idMateria,materia,idGrupo,idHorario,idCiclo):
    if current_user.is_authenticated and current_user.is_profesor():
        c = Calificaciones()
        d = DetalleCalificaciones()
        calificaciones = c.consultaIndividual(noControl)
        idCalificacion = 0;
        for cal in calificaciones:
            if cal.idMateria == idMateria:
                idCalificacion = cal.idCalificacion
        detalleCalificaciones = d.consultaIndividual(idCalificacion)
        g = Grupos()
        grupo = g.consultaIndividual(idGrupo)
        return render_template('calificaciones/listadoCalificaciones.html', idMateria=idMateria,idCiclo=idCiclo,materia=materia,estudiante=estudiante,
                               noControl=noControl,idGrupo=idGrupo,idHorario=idHorario, detalleCalificaciones=detalleCalificaciones,
                               idCalificacion=idCalificacion, grupo=grupo)
    else:
        abort(404)


@app.route('/editarCalificacionEst/<int:idCalificacion>,<string:estudiante>,<string:noControl>,<int:idMateria>,<string:materia>,<int:idCiclo>,<int:idDetalleCalificacion>,<string:grupo>,<int:idGrupo>,<int:idHorario>')
@login_required
def CalifEditar(idCalificacion,estudiante,noControl,idMateria,materia,idCiclo,idDetalleCalificacion,grupo,idGrupo,idHorario):
    if current_user.is_authenticated and current_user.is_profesor():
        d = DetalleCalificaciones()
        bimestre = 0;
        calificacion = 0.0;
        for detalle in d.consultaGeneral():
            if detalle.idDetalleCalificacion == idDetalleCalificacion:
                bimestre=detalle.bimestre
                calificacion=detalle.calificacion
        return render_template('calificaciones/calificacionesEditar.html', idMateria=idMateria,idCiclo=idCiclo,materia=materia,estudiante=estudiante,
                               noControl=noControl,idCalificacion=idCalificacion,idDetalleCalificacion=idDetalleCalificacion, grupo=grupo,
                               bimestre = bimestre,calificacion=calificacion,idHorario=idHorario,idGrupo=idGrupo)
    else:
        abort(404)

@app.route('/EditarCalificaciones', methods=['post'])
@login_required
def EditarCalificaciones():
    if current_user.is_authenticated and current_user.is_profesor():
        d = DetalleCalificaciones()
        d.idDetalleCalificacion=request.form['idDetalleCalificacion']
        d.bimestre=request.form['bimestre']
        d.calificacion=request.form['calificacion']
        d.idCalificacion=request.form['idCalificacion']
        d.actualizar()
        c = Calificaciones()
        c.idCalificacion=request.form['idCalificacion']
        c.noControl = request.form['noControl']
        c.idMateria = request.form['idMateria']
        c.idCiclo = request.form['idCiclo']
        calificacionFinal=0;
        cont=0;
        for detalle in d.consultaGeneral():
            if detalle.idCalificacion == int(request.form['idCalificacion']):
                calificacionFinal+=detalle.calificacion
                cont+=1;
        calificacionFinal/=cont;
        c.calificacionFinal = calificacionFinal
        c.actualizar()

        flash('¡Se han guardado los cambios con éxito!')
        return render_template('calificaciones/calificacionesEditar.html', idMateria=request.form['idMateria'],idCiclo=request.form['idCiclo'],
                               materia=request.form['materia'],estudiante=request.form['estudiante'], noControl=request.form['noControl'],
                               idCalificacion=request.form['idCalificacion'],idDetalleCalificacion=request.form['idDetalleCalificacion'],
                               grupo=request.form['grupo'],bimestre = request.form['bimestre'],calificacion=request.form['calificacion'],
                               idHorario=request.form['idHorario'],idGrupo=request.form['idGrupo'])
    else:
        abort(404)

@app.route('/EliminarCalificacion/<int:idDetalleCalificacion>,<string:estudiante>,<string:noControl>,<int:idMateria>,<string:materia>,<int:idGrupo>,<int:idHorario>,<int:idCiclo>')
@login_required
def EliminarCalificacion(idDetalleCalificacion,estudiante,noControl,idMateria,materia,idGrupo,idHorario,idCiclo):
    if current_user.is_authenticated and current_user.is_profesor():
        d = DetalleCalificaciones()
        d.eliminar(idDetalleCalificacion)

        c = Calificaciones()
        calificaciones = c.consultaIndividual(noControl)
        idCalificacion = 0;
        for cal in calificaciones:
            if cal.idMateria == idMateria:
                idCalificacion = cal.idCalificacion
        detalleCalificaciones = d.consultaIndividual(idCalificacion)
        g = Grupos()
        grupo = g.consultaIndividual(idGrupo)
        flash ('Calificación eliminada con éxito!!')
        return render_template('calificaciones/listadoCalificaciones.html', idMateria=idMateria,idCiclo=idCiclo,materia=materia,estudiante=estudiante,
                               noControl=noControl,idGrupo=idGrupo,idHorario=idHorario, detalleCalificaciones=detalleCalificaciones,
                               idCalificacion=idCalificacion, grupo=grupo)
    else:
        abort(404)

###################################################################################
@app.route('/horarios')
@login_required
def horarios():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        m = Materias()
        p = Profesores()
        h = Horarios()
        g = Grupos()
        u = Usuarios()
        return render_template('horarios/horarios.html', materias=m.consultaGeneral(),
                               profesores=p.consultaGeneral(), horarios=h.consultaGeneral(), grupos=g.consultaGeneral(),
                               usuario=u.consultaGeneral())
    else:
        abort(404)
@app.route('/generarHorario',methods=['post'])
@login_required
def horarioGenerar():
    if current_user.is_authenticated and current_user.is_staff():
        return 'GESTIÓN DE HORARIOS'
    else:
        abort(404)

###################################################################################
@app.route('/inscripciones')
@login_required
def inscripciones():
    if current_user.is_authenticated and (current_user.is_estudiante() or current_user.is_staff()):
        g = Grupos()
        grup = g.consultaGeneral()
        c= cicloEscolar()
        ciclos = c.consultaGeneral()
        act = 0;
        for idc in ciclos:
            act = idc.idCiclo
        e= Estudiantes ()
        est= e.consultaGeneral()
        i = Inscripciones()
        noControl = '';
        for ee in est:
            if current_user.idUsuario == ee.idUsuario:
                noControl=ee.noControl
        gpAC = 0;
        grado = 0;
        for a in i.consultaGeneral():
            if a.noControl == noControl:
                gpAC = a.idGrupo
        for gg in grup:
            if gg.idGrupo == gpAC:
                grado = gg.grado
        return render_template('inscripciones/inscripciones.html', grupos=grup, ciclos=ciclos,actual = act, estudiantes = est, gpActual = gpAC, grado = grado)
    else:
        abort(404)

@app.route('/registrarInscripcion', methods=['post'])
@login_required
def registrarInscripcion():
    if current_user.is_authenticated and (current_user.is_estudiante() or current_user.is_staff()):
        ins = Inscripciones()
        ins.noControl = request.form['noControl']
        ins.idGrupo = request.form['idGrupo']
        ins.idCiclo = request.form['idCiclo']
        ins.insertar()
        flash('Se ha registrado la inscripción con éxito!!')
        return redirect(url_for('inscripciones'))
    else:
        abort(404)

@app.route('/inscripcionesListado')
@login_required
def consultarInscripciones():
    if current_user.is_authenticated and current_user.is_staff():
        i = Inscripciones()
        ins = i.consultaGeneral()
        e = Estudiantes()
        est = e.consultaGeneral()
        u=Usuarios ()
        us= u.consultaGeneral()
        g=Grupos()
        grup=g.consultaGeneral()
        c = cicloEscolar()
        cic = c.consultaGeneral()
        return render_template('inscripciones/inscripcionesListado.html', inscripciones = ins, estudiantes = est, usuarios = us, grupos=grup, ciclos=cic)
    else:
        abort(404)

@app.route('/edicionInscripciones/<int:id>')
@login_required
def Edicioninscripciones(id):
    if current_user.is_authenticated and current_user.is_staff():
        g = Grupos()
        grup = g.consultaGeneral()
        c= cicloEscolar()
        ciclos = c.consultaGeneral()
        e= Estudiantes ()
        est= e.consultaGeneral()
        i = Inscripciones()
        ins=i.consultaIndividual(id)
        u=Usuarios()
        us=u.consultaGeneral()
        return render_template('inscripciones/inscripcionEdicion.html', grupos=grup, ciclos=ciclos, estudiantes=est, inscripcion=ins, usuarios=us)
    else:
        abort(404)
@app.route('/datosEdicionInscripcion', methods=['post'])
@login_required
def datosEdicionInscripcion():
    if current_user.is_authenticated and current_user.is_staff():
        ins = Inscripciones()
        ins.idInscripciones=request.form['idInscripciones']
        ins.noControl = request.form['noControl']
        ins.idGrupo = request.form['idGrupo']
        ins.idCiclo = request.form['idCiclo']
        ins.actualizar()
        g = Grupos()
        grup = g.consultaGeneral()
        c= cicloEscolar()
        ciclos = c.consultaGeneral()
        e= Estudiantes ()
        est= e.consultaGeneral()
        i = Inscripciones()
        ins=i.consultaIndividual(request.form['idInscripciones'])
        u=Usuarios()
        us=u.consultaGeneral()
        flash('Se han guardado los cambios con éxito!!')
        return render_template('inscripciones/inscripcionEdicion.html', grupos=grup, ciclos=ciclos, estudiantes=est, inscripcion=ins, usuarios=us)
    else:
        abort(404)

@app.route('/eliminarInscripcion/<int:id>')
@login_required
def inscripcionesEliminar(id):
    if current_user.is_authenticated and current_user.is_staff():
        i= Inscripciones()
        i.eliminar(id)
        flash('Se ha eliminado la inscripción con éxito!!')
        return redirect(url_for('consultarInscripciones'))
    else:
        abort(404)
#################################################################################
@app.route('/materiasListado')
@login_required
def materiasListado():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        m = Materias()
        mat = m.consultaGeneral()
        return render_template('materias/materiasListado.html', materias=mat)
    else:
        abort(404)

@app.route('/materiaNuevo')
@login_required
def materiaNuevo():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        return render_template('materias/nuevaMateria.html')
    else:
        abort(404)

@app.route('/registrarMateria',methods=['post'])
@login_required
def registrarMateria():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        m = Materias ()
        m.nombre=request.form['nombre']
        m.grado=request.form['grado']
        m.insertar()
        flash('Se ha registrado una nueva materia con éxito!!')
        return render_template('materias/nuevaMateria.html')
    else:
        abort(404)

@app.route('/materiasEditar/<int:id>')
@login_required
def materiasEditar(id):
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        m= Materias()
        return render_template('materias/materiaEditar.html', materia = m.consultaIndividual(id))
    else:
        abort(404)

@app.route('/materiasEliminar/<int:id>')
@login_required
def materiasEliminar(id):
    if current_user.is_authenticated and current_user.is_administrador():
        m= Materias()
        m.eliminar(id)
        mat = m.consultaGeneral()
        flash('Se ha eliminado la materia con éxito!!')
        return render_template('materias/materiasListado.html', materias=mat)
    else:
        abort(404)

@app.route('/materiasObtenerDatos',methods=['post'])
@login_required
def materiasObtenerDatos():
    if current_user.is_authenticated and (current_user.is_administrador() or current_user.is_staff()):
        m= Materias()
        m.idMateria=request.form['idMateria']
        m.nombre=request.form['nombre']
        m.grado=request.form['grado']
        m.actualizar()
        flash('Se han gruardado los cambios con éxito!!')
        return render_template('materias/materiaEditar.html', materia = m.consultaIndividual(request.form['idMateria']))
    else:
        abort(404)

#################################################################################
@app.route('/ciclos')
@login_required
def ciclos():
    if current_user.is_authenticated and current_user.is_administrador():
        c = cicloEscolar()
        ciclos = c.consultaGeneral()
        return render_template('ciclos/ciclosListado.html', ciclos=ciclos)
    else:
        abort(404)

@app.route('/cicloNuevo')
@login_required
def cicloNuevo():
    if current_user.is_authenticated and current_user.is_administrador():
        return render_template('ciclos/cicloNuevo.html')
    else:
        abort(404)

@app.route('/registrarCiclo',methods=['post'])
@login_required
def registrarCiclo():
    if current_user.is_authenticated and current_user.is_administrador():
        c = cicloEscolar ()
        c.nombre=request.form['nombre']
        c.insertar()
        flash('Se ha registrado una nuevo ciclo con éxito!!')
        return render_template('ciclos/cicloNuevo.html')
    else:
        abort(404)

@app.route('/ciclosEditar/<int:id>')
@login_required
def ciclosEditar(id):
    if current_user.is_authenticated and current_user.is_administrador():
        c= cicloEscolar()
        return render_template('ciclos/cicloEditar.html', ciclo = c.consultaIndividual(id))
    else:
        abort(404)

@app.route('/ciclosEliminar/<int:id>')
@login_required
def ciclosEliminar(id):
    if current_user.is_authenticated and current_user.is_administrador():
        c= cicloEscolar()
        c.eliminar(id)
        cic = c.consultaGeneral()
        flash('Se ha eliminado un ciclo con éxito!!')
        return render_template('ciclos/ciclosListado.html', ciclos=cic)
    else:
        abort(404)

@app.route('/ciclosObtenerDatos',methods=['post'])
@login_required
def ciclosObtenerDatos():
    if current_user.is_authenticated and current_user.is_administrador():
        c= cicloEscolar()
        c.idCiclo=request.form['idCiclo']
        c.nombre=request.form['nombre']
        estatus =request.values.get('estatus',False)
        if estatus=="True":
            c.estatus=True
        else:
            c.estatus=False
        c.actualizar()
        flash('Se han gruardado los cambios con éxito!!')
        return render_template('ciclos/cicloEditar.html', ciclo = c.consultaIndividual(request.form['idCiclo']))
    else:
        abort(404)

@app.errorhandler(404)
def error404(e):
    return render_template('comunes/paginaError.html'),404

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)

