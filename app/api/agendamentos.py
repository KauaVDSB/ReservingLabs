from flask import request, jsonify

from app import app
from app.models import Solicitacao

import datetime

@app.route('/api/agendamentos')
def api_agendamentos():
    """
    Endpoint para obter agendamentos de laboratório para um determinado período.
    Retorna os dados em formato JSON.
    """
    # Recebe as datas de início e fim
    start_date_str = request.args.get('start')
    end_date_str = request.args.get('end')

    # Converte as strings de data para objetos datetime
    start_date = datetime.datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
    end_date = datetime.datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))

    # Realiza a query para obter os agendamentos correspondentes
    solicitacoes = Solicitacao.query.filter(
        Solicitacao.data_agendada >= start_date,
        Solicitacao.data_encerramento <= end_date,
        Solicitacao.status == 'Aprovada'
    ).all()

    # Transforma os resultados em um formato JSON (Lido pelo FullCalendar.io)
    agendamentos_json = []
    for solicitacao in solicitacoes:
        agendamentos_json.append({
            'title': f"{solicitacao.lab.nome} - {solicitacao.user.nome}",
            'start': solicitacao.data_agendada.isoformat(),
            'end': solicitacao.data_encerramento.isoformat(),
            'color': '#198754' if solicitacao.lab.status == 'Disponível' else '#dc3545',
            'id': solicitacao.id
        })

    return jsonify(agendamentos_json)
