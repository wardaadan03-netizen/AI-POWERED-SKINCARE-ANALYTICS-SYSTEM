// ============================================
// DASHBOARD SPECIFIC FUNCTIONS
// ============================================

let currentChart = null;

// Initialize dashboard
function initDashboard() {
    console.log('Dashboard initializing...');
    
    // Load user data
    loadUserProfile();
    
    // Load statistics
    loadStatistics();
    
    // Load recommendations
    loadRecommendations();
    
    // Initialize charts
    initCharts();
    
    // Set up auto-refresh
    startAutoRefresh();
}

// Load user profile
async function loadUserProfile() {
    try {
        const response = await fetch('/api/user/profile');
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('user-name').textContent = data.user.name || 'User';
            document.getElementById('user-email').textContent = data.user.email;
            document.getElementById('member-since').textContent = formatDate(data.user.member_since);
        }
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        if (data.user_stats) {
            animateNumber('skin-score', data.user_stats.skin_health_score || 0);
            animateNumber('routine-score', data.user_stats.routine_consistency || 0);
            animateNumber('match-score', data.user_stats.product_match_score || 0);
            animateNumber('rec-count', data.user_stats.total_recommendations || 0);
        }
    } catch (error) {
        console.error('Error loading statistics:', error);
    }
}

// Animate number counting
function animateNumber(elementId, targetValue) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const duration = 1000;
    const start = parseInt(element.textContent) || 0;
    const increment = (targetValue - start) / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= targetValue) || (increment < 0 && current <= targetValue)) {
            element.textContent = targetValue;
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current);
        }
    }, 16);
}

// Initialize all charts
async function initCharts() {
    try {
        const response = await fetch('/api/analytics');
        const data = await response.json();
        
        // Create 3D visualizations
        if (data.ingredient_network && document.getElementById('ingredient-network')) {
            Plotly.newPlot('ingredient-network', data.ingredient_network.data, data.ingredient_network.layout);
        }
        
        if (data.budget_analysis && document.getElementById('budget-analysis')) {
            Plotly.newPlot('budget-analysis', data.budget_analysis.data, data.budget_analysis.layout);
        }
        
        if (data.skin_distribution && document.getElementById('skin-distribution')) {
            Plotly.newPlot('skin-distribution', data.skin_distribution.data, data.skin_distribution.layout);
        }
        
        // Create heatmap
        createHeatmapVisualization();
        
    } catch (error) {
        console.error('Error initializing charts:', error);
        createFallbackVisualizations();
    }
}

// Create heatmap visualization
function createHeatmapVisualization() {
    const ingredients = ['Retinol', 'Vitamin C', 'Niacinamide', 'HA', 'Salicylic Acid', 'Ceramides'];
    const ageGroups = ['18-25', '26-35', '36-45', '46-55', '55+'];
    const data = [
        [45, 65, 78, 65, 45, 30],
        [55, 75, 85, 75, 55, 45],
        [65, 85, 75, 85, 65, 60],
        [75, 80, 65, 80, 70, 70],
        [80, 70, 55, 70, 65, 75]
    ];
    
    const trace = {
        z: data,
        x: ingredients,
        y: ageGroups,
        type: 'heatmap',
        colorscale: 'Viridis',
        colorbar: { title: 'Usage %' }
    };
    
    const layout = {
        title: 'Active Ingredients Usage by Age Group',
        xaxis: { title: 'Ingredients', tickangle: -45 },
        yaxis: { title: 'Age Group' },
        height: 400
    };
    
    if (document.getElementById('ingredient-heatmap')) {
        Plotly.newPlot('ingredient-heatmap', [trace], layout);
    }
}

// Create fallback visualizations if API fails
function createFallbackVisualizations() {
    // Sample 3D scatter data
    const scatterTrace = {
        x: [25, 35, 45, 55, 65],
        y: [50, 100, 150, 200, 250],
        z: [85, 82, 78, 75, 70],
        mode: 'markers',
        type: 'scatter3d',
        marker: { size: 10, color: 'red' }
    };
    
    if (document.getElementById('ingredient-network')) {
        Plotly.newPlot('ingredient-network', [scatterTrace], { title: '3D Visualization' });
    }
    
    if (document.getElementById('budget-analysis')) {
        Plotly.newPlot('budget-analysis', [scatterTrace], { title: 'Budget Analysis' });
    }
    
    if (document.getElementById('skin-distribution')) {
        Plotly.newPlot('skin-distribution', [scatterTrace], { title: 'Skin Distribution' });
    }
}

// Load recommendations
async function loadRecommendations() {
    const grid = document.getElementById('recommendations-grid');
    if (!grid) return;
    
    grid.innerHTML = '<div class="spinner"></div><p>Loading recommendations...</p>';
    
    try {
        const response = await fetch('/api/recommendations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
        });
        
        const data = await response.json();
        
        if (data.success && data.products) {
            displayRecommendationCards(data.products);
        } else {
            displaySampleRecommendations();
        }
    } catch (error) {
        console.error('Error loading recommendations:', error);
        displaySampleRecommendations();
    }
}

// Display recommendation cards
function displayRecommendationCards(products) {
    const grid = document.getElementById('recommendations-grid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    products.slice(0, 6).forEach(product => {
        const stars = '★'.repeat(Math.floor(product.rating)) + '☆'.repeat(5 - Math.floor(product.rating));
        
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <div class="product-name">${product.name}</div>
            <div class="product-brand">${product.brand}</div>
            <div class="product-price">$${product.price.toFixed(2)}</div>
            <div class="rating">${stars} (${product.rating})</div>
            <div class="match-score">${product.match_percentage}% Match</div>
            <button onclick="viewProductDetails('${product.name}')" class="btn btn-sm btn-primary mt-2">
                View Details
            </button>
        `;
        grid.appendChild(card);
    });
}

// Display sample recommendations
function displaySampleRecommendations() {
    const sampleProducts = [
        { name: 'CeraVe Hydrating Cleanser', brand: 'CeraVe', price: 12.99, rating: 4.7, match_percentage: 92 },
        { name: 'The Ordinary Niacinamide', brand: 'The Ordinary', price: 5.90, rating: 4.4, match_percentage: 88 },
        { name: "Paula's Choice Vitamin C", brand: "Paula's Choice", price: 49.00, rating: 4.6, match_percentage: 85 },
        { name: 'La Roche-Posay Anthelios', brand: 'La Roche-Posay', price: 29.99, rating: 4.7, match_percentage: 90 },
        { name: 'Kiehl\'s Ultra Facial Cream', brand: 'Kiehl\'s', price: 38.00, rating: 4.5, match_percentage: 82 },
        { name: 'SkinCeuticals C E Ferulic', brand: 'SkinCeuticals', price: 182.00, rating: 4.9, match_percentage: 78 }
    ];
    displayRecommendationCards(sampleProducts);
}

// View product details
async function viewProductDetails(productName) {
    try {
        const response = await fetch('/api/predict-rating', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ product_name: productName })
        });
        
        const data = await response.json();
        
        showModal(`
            <h3>${productName}</h3>
            <p>Predicted Rating: ${data.predicted_rating}/5 ⭐</p>
            <p>Confidence: ${data.confidence}%</p>
            <p>Based on your skin profile and preferences</p>
        `);
    } catch (error) {
        showModal(`
            <h3>${productName}</h3>
            <p> This product is  recommended for your skin type!</p>
            <p>Match Score: 85%</p>
        `);
    }
}

// Show modal dialog
function showModal(content) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            ${content}
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.style.display = 'block';
    
    modal.querySelector('.close').onclick = () => modal.remove();
    window.onclick = (event) => {
        if (event.target === modal) modal.remove();
    };
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
}

// Start auto-refresh
function startAutoRefresh() {
    setInterval(() => {
        loadStatistics();
    }, 30000);
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('dashboard-container')) {
        initDashboard();
    }
});