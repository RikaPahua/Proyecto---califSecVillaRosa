from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, BLOB, Date

db = SQLAlchemy()

class Usuarios(db.Model):
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

class Estudiantes(db.Model):
    __tablename__='Estudiantes'
    noControl=Column(String(8), primary_key=True)
    idUsuario=Column(Integer)
    fechaNacimiento=Column(Date)
    fechaIngreso=Column(Date)
    promedioGeneral=Column(Integer)

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