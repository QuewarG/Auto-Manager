// dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('myChart').getContext('2d');

    // Retrieve data from data attributes
    var usersCount = document.getElementById('myChart').dataset.usersCount;
    var branchesCount = document.getElementById('myChart').dataset.branchesCount;
    var productsCount = document.getElementById('myChart').dataset.productsCount;
    var ordersCount = document.getElementById('myChart').dataset.ordersCount;

    var chartData = {
        labels: ["Users", "Branches", "Products", "Ordenes"],
        datasets: [{
            label: 'Detalles',
            data: [usersCount, branchesCount, productsCount, ordersCount],
            backgroundColor: [
                'rgb(249, 218, 218)',
                'rgb(254, 226, 254)',
                'rgb(236, 236, 254)',
                'rgb(235, 254, 235)',
            ],
            borderColor: [
                '#ED3833',
                '#812B80',
                '#2046F6',
                '#3A811D',
            ],
            borderWidth: 1
        }]
    };

    var myChart = new Chart(ctx, {
        type: 'bar',
        data: chartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});


// dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    var pieCtx = document.getElementById('pieChart').getContext('2d');

    // Retrieve data from data attributes
    var usersCount = document.getElementById('pieChart').dataset.usersCount;
    var branchesCount = document.getElementById('pieChart').dataset.branchesCount;
    var productsCount = document.getElementById('pieChart').dataset.productsCount;
    var ordersCount = document.getElementById('pieChart').dataset.ordersCount;


    var pieChartData = {
        labels: ["Users", "Branches", "Products", "Orders"],
        datasets: [{
            data: [usersCount, branchesCount, productsCount, ordersCount],
            backgroundColor: [
                '#F88682',
                '#C554C5',
                '#6E8BFF',
                '#7BCF5B',
            ],
            borderColor: [
                '#ED3833',
                '#812B80',
                '#2046F6',
                '#3A811D',
            ],
            borderWidth: 1
        }]
    };

    var pieChart = new Chart(pieCtx, {
        type: 'pie',
        data: pieChartData,
        options: {
            responsive: true,
            maintainAspectRatio: false, // Permite cambiar las dimensiones del gráfico
            layout: {
                padding: {
                    bottom: 20 // Ajusta este valor para cambiar la distancia del gráfico hacia abajo
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    align: 'center', // Centra los labels
                    labels: {
                        font: {
                            size: 14
                        }
                    }
                }
            }
        }
    });
});


/*
// dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    var lineCtx = document.getElementById('lineChart').getContext('2d');

    // Retrieve data from data attributes
    var usersCount = document.getElementById('lineChart').dataset.usersCount;
    var branchesCount = document.getElementById('lineChart').dataset.branchesCount;
    var productsCount = document.getElementById('lineChart').dataset.productsCount;

    var lineChartData = {
        labels: ["Users", "Branches", "Products"],
        datasets: [{
            label: 'Counts',
            data: [usersCount, branchesCount, productsCount],
            fill: false, // No rellenar el área bajo la línea
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 2
        }]
    };

    var lineChart = new Chart(lineCtx, {
        type: 'line',
        data: lineChartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
            // Opciones adicionales si es necesario
        }
    });
});
*/