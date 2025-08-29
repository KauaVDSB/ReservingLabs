import datetime
from app import app, db
from app.models import Laboratorio, Solicitacao


def atualizar_status_laboratorios():
    """
    Função que atualiza o status de cada laboratório com base nos agendamentos.
    Ocorre a cada 5 minutos por um cron job.
    """

    with app.app_context():
        agora = datetime.datetime.now()


        # Encontra e atualiza laboratórios para 'Ocupado'
        solicitacoes_ativas = Solicitacao.query.filter(
            Solicitacao.data_agendada <= agora,  # Solicitações que começaram
            Solicitacao.data_encerramento >= agora,  # Solicitações que ainda estão em andamento
            Solicitacao.status == 'Aprovada'
        ).all()

        for solicitacao in solicitacoes_ativas:
            lab = Laboratorio.query.get(solicitacao.id_lab)
            if lab and lab.status != 'Ocupado':
                lab.status = 'Ocupado'
                db.session.add(lab)


        # Encontra e atualiza laboratórios para 'Disponível'
        laboratorios_ocupados = Laboratorio.query.filter(
            Laboratorio.status == 'Ocupado'
        ).all()
        
        for lab in laboratorios_ocupados:
            solicitacoes_ocorrendo = Solicitacao.query.filter(
                Solicitacao.id_lab == lab.id,
                Solicitacao.data_agendada <= agora,  # Solicitações que começaram
                Solicitacao.data_encerramento > agora,  # Solicitações que ainda estão em andamento
                Solicitacao.status == 'Aprovada'
            ).count()

            # Se não houver solicitações ocorrendo no momento, o status volta para 'Disponível'
            if solicitacoes_ocorrendo == 0:
                lab.status = 'Disponivel'
                db.session.add(lab)
        
        db.session.commit()
        print(f"Status dos laboratórios atualizados às {agora.strftime('%d-%m-%Y %H:%M:%S')}.")
