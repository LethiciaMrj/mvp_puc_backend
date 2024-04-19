
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Consulta
from logger import logger
from schemas.error import ErrorSchema
from schemas.consulta import *
from schemas import *
from flask_cors import CORS



info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
consulta_tag = Tag(name="Consulta", description="Agendamento e cancelamento de consultas")



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/consulta', tags=[consulta_tag],
          responses={"200": ConsultaViewSchema,"409": ErrorSchema, "400": ErrorSchema})
def add_consulta(form: ConsultaSchema):
    """Adiciona uma nova Consulta à base de dados

    Retorna uma representação das consultas 
    """
    data_consulta = datetime.strptime(form.data_consulta, '%Y-%m-%d %H:%M')

    consulta = Consulta(

        nome_paciente=form.nome_paciente,
        nome_medico=form.nome_medico,
        data_consulta=data_consulta)
    
    logger.debug(f"Adicionando consulta: '{consulta.nome_paciente}'")  
        # criando conexão com a base
    
    try:  
      session = Session()
            # adicionando produto
      session.add(consulta)
            # efetivando o camando de adição de novo item na tabela
      session.commit()
      logger.debug(f"Adicionado consulta: '{consulta.nome_paciente}'")
      return apresenta_consulta(consulta), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{consulta.nome_paciente}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar produto '{consulta.nome_paciente}', {error_msg}")
        return {"mesage": error_msg}, 400
    



@app.get('/consultas', tags=[consulta_tag],
         responses={"200": ListagemConsultaSchema })
def get_consultas():
    """Faz a busca por toda consulta cadastrada

    Retorna uma representação da listagem de consultas.
    """
    logger.debug(f"Coletando consultas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    consultas = session.query(Consulta).all()

    if not consultas:
        # se não há consultas cadastradas
        return {"consultas": []}, 200
    else:
        logger.debug(f"%d consultas econtrados" % len(consultas))
        # retorna a representação de consulta
        print(consultas)
        return apresenta_consultas(consultas), 200


@app.get('/consulta', tags=[consulta_tag],
         responses={"200": ConsultaViewSchema,"404": ErrorSchema})
def get_consulta(query: ConsultaBuscaSchema):
    """Faz a busca por uma consulta a partir do nome do paciente 

    Retorna uma representação da consulta.
    """
    id_da_consulta = query.id
    logger.debug(f"Coletando dados sobre consulta #{id_da_consulta}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    consulta = session.query(Consulta).filter(id_da_consulta ==  id_da_consulta).first()
   
    if not consulta:
        # se o produto não foi encontrado
        error_msg = "Consulta não encontrada na base :/"
        logger.warning(f"Erro ao buscar consulta '{id_da_consulta}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Produto econtrado: '{apresenta_consulta}'")
        # retorna a representação de produto
        return apresenta_consulta(consulta), 200



@app.delete('/consulta', tags=[consulta_tag],
            responses={"200": ConsultaDelSchema,"404": ErrorSchema})
def del_consulta(query: ConsultaBuscaSchema):
    """Deleta uma consulta  a partir do nome do paciente informado

    Retorna uma mensagem de confirmação da remoção.
    """
    nome_paciente = unquote(unquote(query.paciente))
    print(nome_paciente)
    logger.debug(f"Deletando consulta #{nome_paciente}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Consulta).filter(Consulta.nome_paciente == nome_paciente).delete()
    session.commit()
    
    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado consulta #{nome_paciente}")
        return {"mesage": "consulta removida", "id": nome_paciente}
    else:
        # se o produto não foi encontrado
        error_msg = "Consulta não encontrada na base :/"
        logger.warning(f"Erro ao deletar consulta #'{nome_paciente}', {error_msg}")
        return {"mesage": error_msg}, 404

   


   