from playwright.sync_api import sync_playwright
from configs.logger import logger
from configs.vars import INDEX_URL

class AccessTokenRetriever:
    def __init__(self):
        self.captured_data = {"access_token": None, "client_id": None}

    def initialize(self, p):
        '''
            Inicializa o browser para o Playwright.
        '''

        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        return browser, page

    def handle_request(self, request):
        """
            Intercepta a requisição e captura os tokens.
        """

        if 'searchOrigin' in request.url:
            logger.info(f"Interceptada a requisição para coletar token no endpoint: {request.url}")
            headers = request.headers
            self.captured_data["access_token"] = headers.get('access_token')
            self.captured_data["client_id"] = headers.get('client_id')

    def token_retriever(self):
        """
            Configura a interceptação e navega na página.
        """
        with sync_playwright() as p:
            browser, page = self.initialize(p)

            # Cria um event listener para mapear as requisições
            page.on("request", self.handle_request)
            page.goto(INDEX_URL)

            # A request para pegar as origens só acontece ao clicar no input.
            page.get_by_placeholder("Origem").click()
            page.get_by_placeholder("Origem").type(text="S", delay=10)

            browser.close()
            p.stop()

            return self.captured_data
