import time
import os
from services.access_token_retriever import AccessTokenRetriever
from services.origins_retriever import OriginsRetriever
from services.trips import Trips
from utils.functions.routes import routes
from configs.logger import logger
from configs.vars import INDEX_URL

if __name__ == "__main__":

    start = time.time()
    logger.info('Coletando o token de autenticação...')
    retriever = AccessTokenRetriever()
    token = retriever.token_retriever()

    if token.get('access_token'):

        logger.info('Coletando todas as origins e destinos para o Top 10 Trechos.')
        origins = OriginsRetriever(token=token)
        cities = origins.hash_cities()

        logger.info('Organizando os trechos para fazer as requisições...')
        trechos = routes(cities=cities)

        os.system('clear')
        logger.info('Coletando as informações das viagens...')
        trip = Trips(routes_list=trechos, token=token)
        trip.fetch_routes()

        end = time.time()
        total = end - start

        logger.info(f'Tempo de execução: {total:.2f}')

    else:
        logger.fatal('Token não foi coletado, debugar a classe AccessTokenRetriever.')
