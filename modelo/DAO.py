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

#MÉTODOS PARA CUESTIONES DE CRUD
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

#MÉTODOS PARA CUESTIONES DE PERFILAMIENTO
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
    promedioGeneral=Column(Integer)
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

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return self.query.get(id)


class Calificaciones(db.Model):
    __tablename__ = 'Calificaciones'
    idDetalleCalificacion=Column(Integer, primary_key=True)
    noControl = Column(String(8), unique=True)
    idMateria = Column(Integer, nullable=False)
    bimestre = Column(Integer, nullable=True)
    calificacion = Column(Float)
    idCiclo = Column(Integer, nullable=False)

    def insertar (self):
        db.session.add(self)
        db.session.commit()