from app import db



# Classes para Professores e Administração
class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    senha = db.Column(db.String(200), nullable=False)
    # def _init_(self, id: int, nome: str, email: str, senha: str):
    #     self.id = id
    #     self.nome = nome
    #     self.email = email
    #     self.senha = senha

# class Admin(db.Model):
#     def _init_(self, id: int, nome: str, email: str, senha: str):
#         self.id = id
#         self.nome = nome
#         self.email = email
#         self.senha = senha

# # Classes para manipulação dos Laboratórios
# class StatusLab:
#     LAB_ATIVO = 1
#     LAB_INDISPONIVEL = 0

# class Laboratorio:
#     def _init_(self, id: int, nome: str, capacidade: int, equipamentos: str, abertura: Horario, fechamento: Horario, status: StatusLab):
#         self.id = id
#         self.nome = nome
#         self.capacidade = capacidade
#         self.equipamentos = equipamentos
#         self.abertura = abertura
#         self.fechamento = fechamento
#         self.status = status

# class SolicitaLab:
#     def _init_(self, id: int, solicitante: str, idLaboratorio: int, data: Data, inicio: Horario, fim: Horario):
#         self.id = id
#         self.solicitante = solicitante
#         self.idLaboratorio = idLaboratorio
#         self.data = data
#         self.inicio = inicio
#         self.fim = fim

# # Coleções Dinâmicas (representadas como listas em Python)
# class LabsCollection:
#     def _init_(self):
#         self.labs = []

# class SolicitacoesCollection:
#     def _init_(self):
#         self.solicitacoes = []




# # Classes para data e horário
# class Data:
#     def _init_(self, dia: int, mes: int, ano: int):
#         self.dia = dia
#         self.mes = mes
#         self.ano = ano

# class Horario:
#     def _init_(self, hora: int, minuto: int):
#         self.hora = hora
#         self.minuto = minuto

