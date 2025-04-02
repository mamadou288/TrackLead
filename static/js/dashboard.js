// Dashboard charts initialization
document.addEventListener('DOMContentLoaded', function() {
    // Get data from hidden inputs
    const nbWon = parseInt(document.getElementById('nb-won').value) || 0;
    const nbInProgress = parseInt(document.getElementById('nb-in-progress').value) || 0;
    const nbLost = parseInt(document.getElementById('nb-lost').value) || 0;

    // Opportunities Chart
    const opportunitiesCtx = document.getElementById('opportunitiesChart').getContext('2d');
    const opportunitiesChart = new Chart(opportunitiesCtx, {
        type: 'doughnut',
        data: {
            labels: ['Gagnées', 'En cours', 'Perdues'],
            datasets: [{
                data: [nbWon, nbInProgress, nbLost],
                backgroundColor: [
                    'rgba(40, 167, 69, 0.8)',
                    'rgba(23, 162, 184, 0.8)',
                    'rgba(220, 53, 69, 0.8)'
                ],
                borderColor: [
                    'rgba(40, 167, 69, 1)',
                    'rgba(23, 162, 184, 1)',
                    'rgba(220, 53, 69, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Get monthly revenue data from the template
    const monthlyRevenue = JSON.parse(document.getElementById('monthly-revenue').value || '[]');
    const months = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'];

    // Revenue Chart
    const revenueCtx = document.getElementById('revenueChart').getContext('2d');
    const revenueChart = new Chart(revenueCtx, {
        type: 'line',
        data: {
            labels: months,
            datasets: [{
                label: 'Revenus (€)',
                data: monthlyRevenue,
                fill: false,
                borderColor: 'rgba(255, 193, 7, 1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value + ' €';
                        }
                    }
                }
            }
        }
    });
}); 