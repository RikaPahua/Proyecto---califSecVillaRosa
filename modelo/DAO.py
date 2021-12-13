from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, BLOB, Date, ForeignKey, Time, Float
from flask_login import UserMixin
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Usuarios(UserMixin,db.Model):
    __tablename__='Usuarios'
    foto=Column(BLOB)
    idUsuario=Column(Integer, primary_key=True)
    nombre=Column(String (100), unique=True)
    sexo=Column(String(1), nullable=False)
    telefono=Column(String(12), nullable=False)
    domicilio=Column(String(50), nullable=False)
    tipo=Column(String(1), nullable=False)
    estatus=Column(Boolean, default=True)
    email=Column(String(50), unique=True)
    clave=Column(String(50), nullable=False)

#MÉTODOS PARA CUESTIONES DE CRUD.


    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual (self,id):
        return self.query.get(id)

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto= self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultaGeneral (self):
        return self.query.all()

    def validar (self, email, clave):
        usuarios=None
        usuarios=self.query.filter(Usuarios.email==email, Usuarios.clave==clave, Usuarios.estatus ==True).first()
        return usuarios


    def consultarEmail(self,email):
        salida={"estatus":"","mensaje":""}
        usuario=None
        usuario=self.query.filter(Usuarios.email==email).first()
        if usuario!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El correo "+email+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El correo "+email+" esta libre."
        return salida

    def consultarTelefono(self,telefono):
        salida={"estatus":"","mensaje":""}
        usuario=None
        usuario=self.query.filter(Usuarios.telefono==telefono).first()
        if usuario!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El telefono "+telefono+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El telefono "+telefono+" esta libre."
        return salida

    def consultarNombre(self,nombre):
        salida={"estatus":"","mensaje":""}
        usuario=None
        usuario=self.query.filter(Usuarios.nombre==nombre).first()
        if usuario!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida

#MÉTODOS PARA CUESTIONES DE PERFILAMIENTO.
    def is_authenticated(self):
        return True

    def is_active(self):
        return self.estatus

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idUsuario

    def is_administrador(self):
        if self.tipo=="A":
            return True
        else:
            return False

    def is_staff(self):
        if self.tipo=="S":
            return True
        else:
            return False

    def is_profesor(self):
        if self.tipo=="P":
            return True
        else:
            return False

    def is_estudiante(self):
        if self.tipo=="E":
            return True
        else:
            return False

class Estudiantes(db.Model):
    __tablename__='Estudiantes'
    noControl=Column(String(8), primary_key=True)
    idUsuario=Column(Integer,ForeignKey('Usuarios.idUsuario'))
    fechaNacimiento=Column(Date)
    fechaIngreso=Column(Date)
    promedioGeneral=Column(Integer,default=10)
    usuario=relationship('Usuarios',backref='estudiantes', lazy="select")

    def consultaGeneral (self):
        return self.query.all()

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual (self,id):
        return self.query.get(id)

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,noControl):
        objeto= self.consultaIndividual(noControl)
        db.session.delete(objeto)
        db.session.commit()

    def consultarNoCont(self,noControl):
        salida={"estatus":"","mensaje":""}
        estudiantes=None
        estudiantes=self.query.filter(Estudiantes.noControl==noControl).first()
        if estudiantes!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El noControl "+noControl+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El noControl "+noControl+" esta libre."
        return salida

class Profesores(db.Model):
    __tablename__='Profesores'
    idProfesor=Column(Integer, primary_key=True)
    idUsuario=Column(Integer,  ForeignKey('Usuarios.idUsuario'))
    especialidad=Column(String(50),nullable=True)
    fechaContratacion=Column(Date, nullable=True)
    cedula = Column(String(50), unique=True)
    usuario=relationship('Usuarios',backref='profesores', lazy="select")

    def consultaGeneral (self):
        return self.query.all()

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual (self,id):
        return self.query.get(id)

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto= self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()


    def consultarCedula(self,cedula):
        salida={"estatus":"","mensaje":""}
        profesores=None
        profesores=self.query.filter(Profesores.cedula==cedula).first()
        if profesores!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El noControl "+cedula+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El noControl "+cedula+" esta libre."
        return salida

class Grupos (db.Model):
    __tablename__='Grupos'
    idGrupo=Column(Integer, primary_key=True)
    nombre=Column(String (2), unique=True)
    grado=Column(Integer, nullable=False)
    capacidad=Column(Integer, nullable=False)

    def consultaGeneral (self):
        return self.query.all()

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual (self,id):
        return self.query.get(id)

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto= self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()
    def consultarGrupos(self,nombre):
        salida={"estatus":"","mensaje":""}
        grupo=None
        grupo=self.query.filter(Grupos.nombre==nombre).first()
        if grupo!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida

class cicloEscolar(db.Model):
    __tablename__ = 'cicloEscolar'
    idCiclo=Column(Integer, primary_key=True)
    nombre=Column(String(9), unique=True)
    estatus=Column(Boolean, default=True)

    def consultaGeneral (self):
        return self.query.all()

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual (self,id):
        return self.query.get(id)

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto= self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarCiclos(self,nombre):
        salida={"estatus":"","mensaje":""}
        cicloEsc=None
        cicloEsc=self.query.filter(cicloEscolar.nombre==nombre).first()
        if cicloEsc!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida

class Inscripciones(db.Model):
    __tablename__ = 'Inscripciones'
    idInscripciones=Column(Integer, primary_key=True)
    noControl=Column(String(8),ForeignKey('Estudiantes.noControl'))
    idGrupo=Column(Integer, ForeignKey('Grupos.idGrupo'))
    idCiclo=Column(Integer, ForeignKey('cicloEscolar.idCiclo'))
    Estudiante=relationship('Estudiantes',backref='inscripciones', lazy="select")

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral (self):
        return self.query.all()

    def consultaIndividual (self,id):
        return self.query.get(id)

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto= self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

class Materias (db.Model):
    __tablename__ = 'Materias'
    idMateria=Column(Integer, primary_key=True)
    nombre=Column(String(20), unique=True)
    grado=Column(Integer, nullable=False)

    def consultaGeneral (self):
        return self.query.all()

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual (self,id):
        return self.query.get(id)

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto= self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarMaterias(self,nombre):
        salida={"estatus":"","mensaje":""}
        materia=None
        materia=self.query.filter(Materias.nombre==nombre).first()
        if materia!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El nombre "+nombre+" ya se encuentra registrado."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El nombre "+nombre+" esta libre."
        return salida

class Horarios(db.Model):
    __tablename__ = 'Horarios'
    idHorario = Column(Integer, primary_key=True)
    idMateria = Column(Integer, nullable=True)
    idProfesor=Column(Integer, nullable=True)
    idGrupo = Column(Integer, nullable=True)
    idCiclo = Column(Integer, nullable=True)
    dia = Column(String(10), nullable=True)
    horarioInicio = Column(Time, nullable=True)
    horarioFin = Column(Time, nullable=True)
    noSalon = Column(Integer, nullable=True)

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto= self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarHorario(self,dia,horarioInicio,idProfesor):
        salida={"estatus":"","mensaje":""}
        horar=None
        horar=self.query.filter((Horarios.dia==dia) , (Horarios.horarioInicio==horarioInicio)  , (Horarios.idProfesor==idProfesor)).first()
        if horar!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="El profesor ya tiene una clase asignada en ese horario."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El horario esta libre."
        return salida

class Calificaciones(db.Model):
    __tablename__ = 'Calificaciones'
    idCalificacion=Column(Integer, primary_key=True)
    noControl = Column(String(8), unique=True)
    idMateria = Column(Integer, nullable=False)
    idCiclo = Column(Integer, nullable=False)
    calificacionFinal = Column(Float)

    def consultaGeneral (self):
        return self.query.all()

    def consultaIndividualC (self,idCalificacion):
        return self.query.get(idCalificacion)

    def consultaIndividual (self, noControl):
        calificaciones =None
        calificaciones =self.query.filter(Calificaciones.noControl == noControl).all()
        return calificaciones

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self,id):
        objeto= self.consultaIndividualC(id)
        db.session.delete(objeto)
        db.session.commit()

class DetalleCalificaciones(db.Model):
    __tablename__ = 'DetalleCalificaciones'
    idDetalleCalificacion = Column(Integer, primary_key=True)
    bimestre = Column(Integer,nullable=False)
    calificacion = Column(Float, nullable=False)
    idCalificacion = Column(Integer,nullable=False)

    def insertar (self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual (self, idCalificacion):
        detalleCalificaciones =None
        detalleCalificaciones =self.query.filter(DetalleCalificaciones.idCalificacion == idCalificacion).all()
        return detalleCalificaciones

    def consultaGeneral (self):
        return self.query.all()

    def actualizar (self):
        db.session.merge(self)
        db.session.commit()

    def consultaIndividualC (self,idDetalleCalificacion):
        return self.query.get(idDetalleCalificacion)

    def eliminar(self,idDetalleCalificacion):
        objeto= self.consultaIndividualC(idDetalleCalificacion)
        db.session.delete(objeto)
        db.session.commit()

    def consultarDetalleCal(self,bimestre,idCalificacion):
        salida={"estatus":"","mensaje":""}
        detalleCal=None
        detalleCal=self.query.filter((DetalleCalificaciones.bimestre==bimestre) , (DetalleCalificaciones.idCalificacion==idCalificacion)).first()
        if detalleCal!=None:
            salida["estatus"]="Error"
            salida["mensaje"]="Ya existe una calificacion asignada en el bimestre."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]="El bimestre esta libre."
        return salida

