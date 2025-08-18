// Estruturas para data e horário

typedef struct {
    int dia, mes, ano;  // DD/MM/AAAA
} Data;

typedef struct {
    int hora, minuto;  // HH:MM
} Horario;


// Estruturas para manipulação dos Laboratórios

typedef enum {
    LAB_ATIVO = 1,
    LAB_INDISPONIVEL = 0  // Ocupado, bloqueado, manutenção
} StatusLab;

typedef struct {
    int id;
    char nome[100];
    int capacidade;
    char equipamentos[256];
    Horario abertura;
    Horario fechamento;
    StatusLab status;
} Laboratorio;

typedef struct {
    int id;
    char solicitante[100];
    int idLaboratorio;
    Data data;
    Horario inicio;
    Horario fim;

} SolicitaLab;


// Coleções Dinâmicas

typedef struct {
    Laboratorio *labs;
    int tamanho, capacidade;
} LabsCollection;

typedef struct {
    SolicitaLab *solicitacoes;
    int tamanho, capacidade;
} SolicitacoesCollection;

