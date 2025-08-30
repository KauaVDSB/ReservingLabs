# Classes para data e horário
#analogo a structs do C
class Data:
    def __init__(self, dia: int, mes: int, ano: int):
        self.dia = dia
        self.mes = mes
        self.ano = ano

class Horario:
    def __init__(self, hora: int, minuto: int):
        self.hora = hora
        self.minuto = minuto

# Classes para Professores e Administração
class Professor:
    def __init__(self, id: int, nome: str, email: str, senha: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

class Admin:
    def __init__(self, id: int, nome: str, email: str, senha: str):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

# Classes para manipulação dos Laboratórios
class StatusLab:
    LAB_ATIVO = 1
    LAB_INDISPONIVEL = 0

class Laboratorio:
    def __init__(self, id: int, nome: str, capacidade: int, equipamentos: str, abertura: Horario, fechamento: Horario, status: StatusLab):
        self.id = id
        self.nome = nome
        self.capacidade = capacidade
        self.equipamentos = equipamentos
        self.abertura = abertura
        self.fechamento = fechamento
        self.status = status

class SolicitaLab:
    def __init__(self, id: int, solicitante: str, idLaboratorio: int, data: Data, inicio: Horario, fim: Horario):
        self.id = id
        self.solicitante = solicitante
        self.idLaboratorio = idLaboratorio
        self.data = data
        self.inicio = inicio
        self.fim = fim

# Coleções Dinâmicas (representadas como listas em Python)
class LabsCollection:
    def __init__(self):
        self.labs = []

class SolicitacoesCollection:
    def __init__(self):
        self.solicitacoes = []