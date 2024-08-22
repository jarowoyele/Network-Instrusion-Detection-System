let trafficChart, protocolChart, intrusionChart, packetSizeChart;

function updateDashboard() {
    fetch('/api/packets')
        .then(response => response.json())
        .then(data => {
            updatePacketTable(data);
            updateTrafficChart(data);
            updateProtocolChart(data);
            updateIntrusionChart(data);
            updatePacketSizeChart(data);
        });

    fetch('/api/alerts')
        .then(response => response.json())
        .then(data => {
            updateAlerts(data);
        });
}

function updatePacketTable(packets) {
    const tbody = document.querySelector('#packetsTable tbody');
    tbody.innerHTML = '';
    packets.forEach(packet => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${new Date(packet.timestamp).toLocaleString()}</td>
            <td>${packet.protocol_type}</td>
            <td>${packet.is_intrusion ? 'Yes' : 'No'}</td>
        `;
        tbody.appendChild(row);
    });
}

function updateTrafficChart(packets) {
    const labels = packets.map(p => new Date(p.timestamp).toLocaleTimeString());
    const data = packets.map(p => p.header_length);

    if (!trafficChart) {
        const ctx = document.getElementById('trafficChart').getContext('2d');
        trafficChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Traffic Volume',
                    data: data,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Packet Size (bytes)'
                        }
                    }
                }
            }
        });
    } else {
        trafficChart.data.labels = labels;
        trafficChart.data.datasets[0].data = data;
        trafficChart.update();
    }
}
function updateProtocolChart(packets) {
    const protocolCounts = {};
    packets.forEach(p => {
        protocolCounts[p.protocol_type] = (protocolCounts[p.protocol_type] || 0) + 1;
    });

    const labels = Object.keys(protocolCounts);
    const data = Object.values(protocolCounts);

    if (!protocolChart) {
        const ctx = document.getElementById('protocolChart').getContext('2d');
        protocolChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(255, 205, 86)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Protocol Distribution'
                    }
                }
            }
        });
    } else {
        protocolChart.data.labels = labels;
        protocolChart.data.datasets[0].data = data;
        protocolChart.update();
    }
}

function updateIntrusionChart(packets) {
    const intrusionCounts = {
        'Normal': 0,
        'Intrusion': 0
    };
    packets.forEach(p => {
        if (p.is_intrusion) {
            intrusionCounts['Intrusion']++;
        } else {
            intrusionCounts['Normal']++;
        }
    });

    const labels = Object.keys(intrusionCounts);
    const data = Object.values(intrusionCounts);

    if (!intrusionChart) {
        const ctx = document.getElementById('intrusionChart').getContext('2d');
        intrusionChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgb(75, 192, 192)',
                        'rgb(255, 99, 132)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Intrusion Detection'
                    }
                }
            }
        });
    } else {
        intrusionChart.data.datasets[0].data = data;
        intrusionChart.update();
    }
}

function updatePacketSizeChart(packets) {
    const sizeBins = {
        '0-100': 0,
        '101-500': 0,
        '501-1000': 0,
        '1001+': 0
    };

    packets.forEach(p => {
        if (p.header_length <= 100) sizeBins['0-100']++;
        else if (p.header_length <= 500) sizeBins['101-500']++;
        else if (p.header_length <= 1000) sizeBins['501-1000']++;
        else sizeBins['1001+']++;
    });

    const labels = Object.keys(sizeBins);
    const data = Object.values(sizeBins);

    if (!packetSizeChart) {
        const ctx = document.getElementById('packetSizeChart').getContext('2d');
        packetSizeChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Packet Size Distribution',
                    data: data,
                    backgroundColor: 'rgb(153, 102, 255)',
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } else {
        packetSizeChart.data.datasets[0].data = data;
        packetSizeChart.update();
    }
}

function updateAlerts(alerts) {
    const alertsList = document.getElementById('alertsList');
    alertsList.innerHTML = '';
    alerts.forEach(alert => {
        const li = document.createElement('li');
        li.textContent = `${new Date(alert.timestamp).toLocaleString()}: ${alert.message} (Severity: ${alert.severity})`;
        alertsList.appendChild(li);
    });
}

// Update dashboard every 5 seconds
setInterval(updateDashboard, 10000);

// Initial update
updateDashboard();