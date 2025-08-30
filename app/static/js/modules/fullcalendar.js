// Cria objeto de Cache para guardar dados
const eventCache = {};

function getCacheKey(start, end) {
    return `${start.toISOString()}_${end.toISOString()}`;
}


document.addEventListener('DOMContentLoaded', function(){
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initial_view: 'dayGridMonth',
        locale: 'pt-br',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        buttonText: {
            today: 'Hoje',
            month: 'Mês',
            week: 'Semana',
            day: 'Dia'
        },
        height: 'auto',
        events: function(fetchInfo, successCallback, failureCallback){
            // Cria chave de cache a partir das datas de inicio e fim
            const cacheKey = getCacheKey(fetchInfo.start, fetchInfo.end);

            // Verifica se os dados já estão em cache e retorna se existir
            if (eventCache[cacheKey]) {
                successCallback(eventCache[cacheKey]);
                console.log("Dados carregados do cache para o período:", cacheKey);
                return;
            }

            // Se não estiver em cache, chama a rota e salva os dados em cache
            fetch(`/api/agendamentos?start=${fetchInfo.startStr}&end=${fetchInfo.endStr}`)
                .then(response => response.json())
                .then(data => {
                    // 
                    eventCache[cacheKey] = data;
                    console.log("Dados buscados da API e armazenados no cache para o período:", cacheKey);
                    successCallback(data);
                })
                .catch(error => {
                    console.error("Erro ao buscar agendamentos:", error);
                    alert('Ocorreu um erro ao buscar os agendamentos.');
                    failureCallback();
                });
        },
        // Mostre os detalhes do evento ao clicar
        eventClick: function(info) {
            const event = info.event;
            alert(
                'Laboratório ' + event.title + '\n' +
                'Início: ' + event.start.toLocaleString() + '\n' +
                'Fim: ' + event.end.toLocaleString()
            );
        },

        // Aparência dos eventos
        eventDidMount: function(info) {
            const event = info.event;
            if (event.extendedProps.status === 'Aprovada') {
                info.el.style.backgroundColor = '#198754';  // Verde para 'Aprovada'
            }
        }
    });

    calendar.render();
});