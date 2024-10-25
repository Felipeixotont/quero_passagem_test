import logging
from colorama import Fore, Style, init

# Inicializa o colorama (para suporte cross-platform)
init(autoreset=True)

# Cria um logger
logger = logging.getLogger("MeuLoggerPersonalizado")
logger.setLevel(logging.DEBUG)  # Define o nível de log

# Dicionário de cores para cada nível de log
COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.RED + Style.BRIGHT,
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        log_color = COLORS.get(record.levelno, Fore.WHITE)  # Cor padrão: Branco
        log_message = super().format(record)  # Formata a mensagem
        return f"{log_color}{log_message}{Style.RESET_ALL}"  # Aplica a cor

# Cria manipulador para escrever em um arquivo (sem cores)
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.ERROR)  # Apenas erros e críticos
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# Cria manipulador para console (com cores)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Todos os logs
console_formatter = ColorFormatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# Adiciona manipuladores ao logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
