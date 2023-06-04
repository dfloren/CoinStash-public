const data = {
    labels: [],
    datasets: [{
        label: 'Portfolio',
        data: [],
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(148, 0, 211)',
            'rgb(255, 127, 0)',
            'rgb(75, 0, 130)',
            'rgb(255, 255, 0)',
            'rgb(0, 0, 255)',
            'rgb(0, 255, 0)',
        ],
        hoverOffset: 4
    }]
};

const config = {
    type: 'doughnut',
    data: data,
};


function loadChart() {
    const myChart = new Chart(document.getElementById('homeChart'), config);

    $.ajax({
        method: "GET",
        url: "http://127.0.0.1:8000/chart_data"
    })
        .done(function(chart_info) {
            for (let key in chart_info) {
                myChart.data.labels.push(key)
                myChart.data.datasets.forEach((dataset) => {
                    dataset.data.push(chart_info[key]);
                });
                myChart.update()
            }
            config.data.datasets.forEach(dataset => {
                if (dataset.data.every(el => el === 0)) {
                    $('#homechart_div').attr('hidden', '')
                } else {
                    $('#homechart_div').removeAttr('hidden')
                }
            })
        });
}

loadChart()