document.addEventListener('DOMContentLoaded', () => {
    initializeSourceSelection();
    fetchDashboardData();
    setInterval(fetchDashboardData, 30000);
});

function initializeSourceSelection() {
    const sourceItems = document.querySelectorAll('.source-item');
    sourceItems.forEach(item => {
        item.addEventListener('click', () => {
            // Remove active state from all sources
            sourceItems.forEach(s => s.classList.remove('active'));
            // Add active state to clicked source
            item.classList.add('active');
            // Update filters for selected source
            updateFiltersForSource(item.querySelector('span').textContent);
        });
    });
}

function updateFiltersForSource(sourceName) {
    const filterColumn = document.querySelector('.filter-column');
    const filterContent = getFilterConfigForSource(sourceName);
    
    filterColumn.innerHTML = `
        <h3>Active Filters <span class="filter-count">${filterContent.filterCount}</span></h3>
        <div class="filter-section">
            ${filterContent.filters}
        </div>
    `;
}

function getFilterConfigForSource(sourceName) {
    const configs = {
        'YouTube': {
            filterCount: 4,
            filters: `
                <div class="filter-group">
                    <label class="filter-label">Content Type</label>
                    <div class="checkbox-group">
                        <label><input type="checkbox"> Shorts</label>
                        <label><input type="checkbox"> Full Videos</label>
                        <label><input type="checkbox"> Live Streams</label>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Duration</label>
                    <input type="range" min="0" max="60" class="filter-range">
                    <span class="range-value">< 30 min</span>
                </div>
            `
        },
        'Facebook Marketplace': {
            filterCount: 5,
            filters: `
                <div class="filter-group">
                    <label class="filter-label">Price Range</label>
                    <div class="range-inputs">
                        <input type="number" placeholder="Min">
                        <input type="number" placeholder="Max">
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Location Radius</label>
                    <select class="filter-select">
                        <option>5 miles</option>
                        <option>10 miles</option>
                        <option>25 miles</option>
                    </select>
                </div>
            `
        },
        'Twitter': {
            filterCount: 7,
            filters: `
                <div class="filter-group">
                    <label class="filter-label">Content Type</label>
                    <div class="checkbox-group">
                        <label><input type="checkbox" checked> Text</label>
                        <label><input type="checkbox" checked> Images</label>
                        <label><input type="checkbox" checked> Videos</label>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Bias Filter</label>
                    <select class="filter-select">
                        <option>All Content</option>
                        <option>Left Leaning</option>
                        <option>Center</option>
                        <option>Right Leaning</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Keywords</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add keyword and press Enter">
                        <div class="tags">
                            <span class="tag">example<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Accounts</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add @username">
                        <div class="tags">
                            <span class="tag">@example<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Topics</label>
                    <div class="checkbox-group scrollable">
                        <label><input type="checkbox"> Technology</label>
                        <label><input type="checkbox"> Politics</label>
                        <label><input type="checkbox"> Science</label>
                        <label><input type="checkbox"> Entertainment</label>
                        <label><input type="checkbox"> Sports</label>
                    </div>
                </div>
            `
        }
        // Add more source-specific filter configurations
    };

    return configs[sourceName] || {
        filterCount: 0,
        filters: '<div class="no-filters">No specific filters available</div>'
    };
}

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