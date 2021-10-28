from flask import Flask,render_template
app = Flask(__name__, template_folder='../vista',static_folder='../static')

@app.route('/')
def login():
    return render_template('comunes/login.html')

@app.route('/recopilarDatosLogin',methods=['post'])
def recopilarDatosLogin():
    #nombreUsuario = request.form['nombreUsuario']
    #return 'Se verificara si existe el usuario '+nombreUsuario
    return render_template('comunes/index.html')

@app.route('/Index')
def index():
    return render_template('comunes/index.html')

###################################################################################
@app.route('/administrativos')
def administrativosListado():
    return render_template('administrativos/administrativosListado.html')

@app.route('/administrativosNuevo')
def administrativosNuevo():
    return render_template('administrativos/administrativoNuevo.html')

@app.route('/administrativosEditar')
def administrativosEditar():
    return render_template('administrativos/administrativoEditar.html')

@app.route('/administrativosEliminar')
def administrativosEliminar():
    return 'SE HA ELIMINADO UN USUARIO ADMINISTRATIVO'

@app.route('/administrativosDatosNuevo',methods=['post'])
def administrativosDatosNuevo():
    return 'SE HA REGISTRADO UN NUEVO USUARIO ADMINISTRATIVO'

@app.route('/administrativosDatosEdicion',methods=['post'])
def administrativosDatosEdicion():
    return 'SE HAN GUARDADO LOS DATOS'

@app.route('/administrativoPerfil')
def administrativoPerfil():
    return render_template('administrativos/administrativoEditar.html')
###################################################################################
@app.route('/estudiantes')
def estudiantesListado():
    return render_template('estudiantes/estudiantesListado.html')

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
    return render_template('profesores/profesoresListado.html')

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
    return render_template('grupos/gruposListado.html')

@app.route('/grupoCalificaciones')
def grupoCalificaciones():
    return render_template('grupos/grupoCalificaciones.html')
###################################################################################
@app.route('/horarios')
def horarios():
    return render_template('horarios/horarios.html')
###################################################################################
@app.route('/inscripciones')
def inscripciones():
    return render_template('inscripciones/inscripciones.html')


@app.route('/registrarInscripcion', methods=['post'])
def registrarInscripcion():
    return 'SE HA REALIZADO UNA INSCRIPCIÓN'


if __name__ == '__main__':
    app.run(debug=True)