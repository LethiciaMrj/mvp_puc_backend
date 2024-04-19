from pydantic import BaseModel
from typing import List
from model.consulta import Consulta
from datetime import datetime


class ConsultaSchema(BaseModel):
    """ Define como uma nova a ser consulta inserida deve ser representado
    """
    id_da_consulta: int = 233
    nome_paciente: str ="dr Leandro"
    nome_medico: str = "Dra Lethicia "
    data_consulta: datetime = "2024-08-01 08:11"
    


class ConsultaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    paciente: str = "Lethicia"


class ListagemConsultaSchema(BaseModel):
    """ Define como uma listagem de consultas será retornada.
    """
    Consulta:List[ConsultaSchema]


def apresenta_consultas(consultas: List[Consulta]):
    """ Retorna uma representação dos dados da consulta seguindo o schema definido em
        ConsultaViewSchema.
    """
    result = []
    for consulta in consultas:
        result.append({
          "nome_paciente": consulta.nome_paciente,
          "nome_medico": consulta.nome_medico,
          "data_consulta": consulta.data_consulta,
            
        })

    return {"consultas": result}


class ConsultaViewSchema(BaseModel):
    """ Define como a consulta será retornada:
    """
    id_da_consulta: int = 233
    nome_paciente: str ="dr Leandro"
    nome_medico: str = "Dra Lethicia "
    data_consulta: datetime = "2024-08-01 08:11"
    

class ConsultaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    paciente: str

def apresenta_consulta(consulta: Consulta):
    """ Retorna uma representação da consulta seguindo o schema definido em
        ConsultaViewSchema.
    """
    return {
          "nome_paciente": consulta.nome_paciente,
          "nome_medico": consulta.nome_medico,
          "data_consulta": consulta.data_consulta
        
    }
