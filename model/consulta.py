from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from  model import Base

class Consulta(Base):
    __tablename__ = 'consulta'

    id = Column("pk_consulta", Integer, primary_key=True)
    nome_paciente = Column(String(140), unique=True)
    nome_medico = Column(String(140), unique=True)
    data_consulta = Column(DateTime, default=datetime.now())


   

    def __init__(self, nome_paciente:str, nome_medico:str,
                 data_consulta:datetime):
        """
        Cria a consulta 
        """
        self.id_da_consulta = id
        self.nome_paciente =  nome_paciente
        self.nome_medico =  nome_medico
        self.data_consulta = data_consulta if data_consulta else datetime.now() 
       
    def __repr__(self):
        return f"Consulta(id={self.id}, nome_paciente='{self.nome_paciente}', nome_medico='{self.nome_medico}', data_consulta='{self.data_consulta}')"
