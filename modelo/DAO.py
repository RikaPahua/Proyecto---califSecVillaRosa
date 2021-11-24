from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, BLOB, Date
from flask_login import UserMixin

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

    def is_admin(self):
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
    idUsuario=Column(Integer)
    fechaNacimiento=Column(Date)
    fechaIngreso=Column(Date)
    promedioGeneral=Column(Integer)

    def consultaGeneral (self):
        return self.query.all()

class Profesores(db.Model):
    __tablename__='Profesores'
    idProfesor=Column(Integer, primary_key=True)
    idUsuario=Column(Integer)
    especialidad=Column(String(50),nullable=True)
    fechaContratacion=Column(Date, nullable=True)
    cedula=Column(String(8),nullable=True,unique=True)

    def consultaGeneral (self):
        return self.query.all()

class Grupos (db.Model):
    __tablename__='Grupos'
    idGrupo=Column(Integer, primary_key=True)
    nombre=Column(String (2), unique=True)
    grado=Column(Integer, nullable=False)
    capacidad=Column(Integer, nullable=False)

    def consultaGeneral (self):
        return self.query.all()


class Inscripciones(db.Model):
    __tablename__ = 'Inscripciones'
    idInscripciones=Column(Integer, primary_key=True)
    noControl=Column(String(8), unique=True)
    idGrupo=Column(Integer, nullable=False)
    idCiclo=Column(Integer, nullable=False)

    def insertar (self):
        db.session.add(self)
        db.session.commit()
