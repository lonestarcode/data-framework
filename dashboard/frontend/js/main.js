document.addEventListener('DOMContentLoaded', () => {
    fetchDashboardData();
    setInterval(fetchDashboardData, 30000);
});

async function fetchDashboardData() {
    try {
        const response = await fetch('http://localhost:5000/api/data');
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error:', error);
    }
}

function updateDashboard(data) {
    // Update metrics
    document.getElementById('totalUsers').textContent = data.stats.users;
    document.getElementById('activeUsers').textContent = data.stats.active;
    document.getElementById('totalTasks').textContent = data.stats.tasks;

    // Update activity list
    const activityList = document.getElementById('activityList');
    activityList.innerHTML = data.recent_activity
        .map(activity => `
            <div class="activity-item">
                <strong>${activity.user}</strong> - ${activity.action}
                <span class="time">${activity.time}</span>
            </div>
        `)
        .join('');
}