// dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('myChart').getContext('2d');

    // Retrieve data from data attributes
    var usersCount = document.getElementById('myChart').dataset.usersCount;
    var branchesCount = document.getElementById('myChart').dataset.branchesCount;
    var productsCount = document.getElementById('myChart').dataset.productsCount;

    var chartData = {
        labels: ["Users", "Branches", "Products"],
        datasets: [{
            label: 'Detalles',
            data: [usersCount, branchesCount, productsCount],
            backgroundColor: [
                'rgb(249, 218, 218)',
                'rgb(254, 226, 254)',
                'rgb(236, 236, 254)'
            ],
            borderColor: [
                '#ED3833',
                '#812B80',
                '#2046F6'
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

    var pieChartData = {
        labels: ["Users", "Branches", "Products"],
        datasets: [{
            data: [usersCount, branchesCount, productsCount],
            backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(75, 192, 192, 0.7)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(75, 192, 192, 1)'
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