import sys
import os
from configs.logger import logger
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf(file_name: str, trips: dict):
    # Cria o PDF com o nome especificado

    os.makedirs('files', exist_ok=True)

    path = f'files/{file_name}.pdf'

    # Inicializa o PDF
    c = canvas.Canvas(path, pagesize=A4)

    # Configurações iniciais
    width, height = A4
    margem_inferior = 50  # Margem para evitar corte
    espacamento_linha = 20  # Espaçamento entre linhas
    altura_bloco_viagem = espacamento_linha * 6
    y = height - 50  # Define a posição inicial no eixo Y

    # Centraliza o título usando a width da página
    c.setFont("Helvetica-Bold", 16)
    title = file_name.replace("-", " - ")
    x_title = (width - c.stringWidth(title, "Helvetica-Bold", 16)) / 2
    c.drawString(x_title, y, title)  # Ex.: SÃO PAULO - BELO HORIZONTE

    # Adiciona as informações de cada viagem
    c.setFont("Helvetica", 12)
    y -= 40  # Move um pouco para baixo

    # Função para verificar se há espaço suficiente
    def verifica_espaco(altura_necessaria):
        nonlocal y
        if y < margem_inferior + altura_necessaria:
            c.showPage()  # Cria uma nova página
            c.setFont("Helvetica", 12)  # Redefine a fonte
            y = height - 50  # Redefine a posição inicial da nova página

    for key,value in trips.items():

        verifica_espaco(espacamento_linha)  # Verifica espaço necessário

        c.drawString(50, y, f"Dia {key}:")
        y -= 40

        for trip in value:
            verifica_espaco(altura_bloco_viagem)  # Verifica se o bloco cabe na página atual

            c.drawString(50, y, f"Classe: {trip.get('trip_class').upper()}")
            y -= 20
            c.drawString(50, y, f"Origem: {trip.get('origin')}")
            y -= 20
            c.drawString(50, y, f"Destino: {trip.get('destiny')}")
            y -= 20
            c.drawString(50, y, f"Preço = {trip.get('price'):.2f}")
            y -= 20
            c.drawString(50, y, f"Horário saída = {trip.get('departure_time')}")
            y -= 20
            c.drawString(50, y, f"Horário chegada = {trip.get('departure_arrival')}")
            y -= 40  # Espaçamento entre viagens

    # Finaliza e salva o PDF
    logger.info('PDF gerado com sucesso!')
    c.showPage()
    c.save()
