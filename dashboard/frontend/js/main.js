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
    const configList = document.querySelector('.config-list');
    const filterColumn = document.querySelector('.filter-column');
    const filterContent = getFilterConfigForSource(sourceName);
    
    // Update saved configurations
    configList.innerHTML = getConfigurationsForSource(sourceName);
    
    // Update filters
    filterColumn.innerHTML = `
        <div class="filter-section">
            ${filterContent.filters}
        </div>
    `;
}

function getConfigurationsForSource(sourceName) {
    const configs = {
        'YouTube': `
            <div class="config-item">
                <span class="config-name">Python Programming</span>
                <div class="config-actions">
                    <button class="icon-button" title="Load Configuration">
                        <i class="fas fa-upload"></i>
                    </button>
                    <button class="icon-button" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="config-item">
                <span class="config-name">Call of Duty</span>
                <div class="config-actions">
                    <button class="icon-button" title="Load Configuration">
                        <i class="fas fa-upload"></i>
                    </button>
                    <button class="icon-button" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="config-item">
                <span class="config-name">Louisville Basketball</span>
                <div class="config-actions">
                    <button class="icon-button" title="Load Configuration">
                        <i class="fas fa-upload"></i>
                    </button>
                    <button class="icon-button" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `,
        'Twitter': `
            <div class="config-item">
                <span class="config-name">NFL</span>
                <div class="config-actions">
                    <button class="icon-button" title="Load Configuration">
                        <i class="fas fa-upload"></i>
                    </button>
                    <button class="icon-button" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="config-item">
                <span class="config-name">Stock Market News</span>
                <div class="config-actions">
                    <button class="icon-button" title="Load Configuration">
                        <i class="fas fa-upload"></i>
                    </button>
                    <button class="icon-button" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `,
        // ... other sources
    };

    return configs[sourceName] || '';
}

function getFilterConfigForSource(sourceName) {
    const configs = {
        'YouTube': {
            filterCount: 11,
            filters: `
                <div class="filter-group">
                    <label class="filter-label">Time Posted</label>
                    <select class="filter-select">
                        <option>Any time</option>
                        <option>Last hour</option>
                        <option>Today</option>
                        <option>This week</option>
                        <option>This month</option>
                        <option>This year</option>
                    </select>
                </div>
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
                <div class="filter-group">
                    <label class="filter-label">Keywords</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add keyword to include">
                        <div class="tags">
                            <span class="tag">tutorial<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group exclude">
                    <label class="filter-label exclude">Exclude Keywords</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add keyword to exclude">
                        <div class="tags">
                            <span class="tag">spam<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Channels</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add channel to include">
                        <div class="tags">
                            <span class="tag">@example<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group exclude">
                    <label class="filter-label exclude">Exclude Channels</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add channel to exclude">
                        <div class="tags">
                            <span class="tag">@blocked<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Topics</label>
                    <select class="filter-select">
                        <option>All Topics</option>
                        <option>Technology</option>
                        <option>Gaming</option>
                        <option>Education</option>
                        <option>Entertainment</option>
                        <option>Music</option>
                        <option>News</option>
                        <option>Sports</option>
                        <option>Politics</option>
                        <option>Science</option>
                        <option>Business</option>
                    </select>
                </div>
                <div class="filter-group exclude">
                    <label class="filter-label exclude">Exclude Topics</label>
                    <select class="filter-select">
                        <option>None</option>
                        <option>Technology</option>
                        <option>Gaming</option>
                        <option>Education</option>
                        <option>Entertainment</option>
                        <option>Music</option>
                        <option>News</option>
                        <option>Sports</option>
                        <option>Politics</option>
                        <option>Science</option>
                        <option>Business</option>
                    </select>
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
            filterCount: 8,
            filters: `
                <div class="filter-group">
                    <label class="filter-label">Time Posted</label>
                    <select class="filter-select">
                        <option>Any time</option>
                        <option>Last hour</option>
                        <option>Today</option>
                        <option>This week</option>
                        <option>This month</option>
                        <option>This year</option>
                    </select>
                </div>
                <div class="filter-group exclude">
                    <label class="filter-label exclude">Exclude Time Range</label>
                    <select class="filter-select">
                        <option>None</option>
                        <option>Older than a week</option>
                        <option>Older than a month</option>
                        <option>Older than a year</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Content Type</label>
                    <div class="checkbox-group">
                        <label><input type="checkbox" checked> Text</label>
                        <label><input type="checkbox" checked> Images</label>
                        <label><input type="checkbox" checked> Videos</label>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Keywords</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add keyword to include">
                        <div class="tags">
                            <span class="tag">example<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group exclude">
                    <label class="filter-label exclude">Exclude Keywords</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add keyword to exclude">
                        <div class="tags">
                            <span class="tag">spam<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Accounts</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add @username to include">
                        <div class="tags">
                            <span class="tag">@example<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group exclude">
                    <label class="filter-label exclude">Exclude Accounts</label>
                    <div class="tag-input">
                        <input type="text" placeholder="Add @username to exclude">
                        <div class="tags">
                            <span class="tag">@blocked<i class="fas fa-times"></i></span>
                        </div>
                    </div>
                </div>
                <div class="filter-group">
                    <label class="filter-label">Topics</label>
                    <select class="filter-select">
                        <option>All Topics</option>
                        <option>Technology</option>
                        <option>Gaming</option>
                        <option>Education</option>
                        <option>Entertainment</option>
                        <option>Music</option>
                        <option>News</option>
                        <option>Sports</option>
                        <option>Politics</option>
                        <option>Science</option>
                        <option>Business</option>
                    </select>
                </div>
                <div class="filter-group exclude">
                    <label class="filter-label exclude">Exclude Topics</label>
                    <select class="filter-select">
                        <option>None</option>
                        <option>Technology</option>
                        <option>Gaming</option>
                        <option>Education</option>
                        <option>Entertainment</option>
                        <option>Music</option>
                        <option>News</option>
                        <option>Sports</option>
                        <option>Politics</option>
                        <option>Science</option>
                        <option>Business</option>
                    </select>
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
                <div class="filter-group exclude">
                    <label class="filter-label exclude">Exclude Bias</label>
                    <select class="filter-select">
                        <option>None</option>
                        <option>Left Leaning</option>
                        <option>Center</option>
                        <option>Right Leaning</option>
                    </select>
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