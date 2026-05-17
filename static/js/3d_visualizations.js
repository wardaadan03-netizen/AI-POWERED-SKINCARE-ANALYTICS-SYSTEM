// Create 3D Scatter Plot
function create3DScatterPlot(data, elementId) {
    const trace = {
        x: data.age,
        y: data.budget,
        z: data.satisfaction,
        mode: 'markers',
        type: 'scatter3d',
        marker: {
            size: data.size || 5,
            color: data.color,
            colorscale: 'Viridis',
            showscale: true,
            colorbar: {
                title: 'Skin Type'
            }
        },
        text: data.skin_types,
        hoverinfo: 'text'
    };
    
    const layout = {
        title: 'Age vs Budget vs Satisfaction (3D)',
        scene: {
            xaxis: { title: 'Age (years)' },
            yaxis: { title: 'Budget (USD)' },
            zaxis: { title: 'Satisfaction (%)' }
        },
        height: 500,
        margin: { l: 0, r: 0, b: 0, t: 50 }
    };
    
    Plotly.newPlot(elementId, [trace], layout, { responsive: true });
}

// Create 3D Surface Plot
function create3DSurfacePlot(zData, xLabels, yLabels, elementId) {
    const trace = {
        z: zData,
        x: xLabels,
        y: yLabels,
        type: 'surface',
        colorscale: 'Viridis',
        colorbar: {
            title: 'Satisfaction %'
        }
    };
    
    const layout = {
        title: 'Satisfaction Surface Plot',
        scene: {
            xaxis: { title: 'Budget Tier' },
            yaxis: { title: 'Age Group' },
            zaxis: { title: 'Satisfaction (%)' }
        },
        height: 500,
        margin: { l: 0, r: 0, b: 0, t: 50 }
    };
    
    Plotly.newPlot(elementId, [trace], layout, { responsive: true });
}

// Create 3D Network Graph
function create3DNetworkGraph(nodes, edges, elementId) {
    // Extract node positions
    const x = nodes.map(n => n.x);
    const y = nodes.map(n => n.y);
    const z = nodes.map(n => n.z);
    
    // Create edge traces
    const edgeTraces = [];
    edges.forEach(edge => {
        const fromNode = nodes[edge.from];
        const toNode = nodes[edge.to];
        
        edgeTraces.push({
            x: [fromNode.x, toNode.x],
            y: [fromNode.y, toNode.y],
            z: [fromNode.z, toNode.z],
            mode: 'lines',
            type: 'scatter3d',
            line: { color: '#888', width: 2 },
            hoverinfo: 'none'
        });
    });
    
    // Create node trace
    const nodeTrace = {
        x: x,
        y: y,
        z: z,
        mode: 'markers+text',
        type: 'scatter3d',
        marker: {
            size: nodes.map(n => n.size || 10),
            color: nodes.map(n => n.color || '#667eea'),
            symbol: 'circle'
        },
        text: nodes.map(n => n.name),
        textposition: 'top center',
        hoverinfo: 'text'
    };
    
    const traces = [...edgeTraces, nodeTrace];
    
    const layout = {
        title: 'Ingredient Co-occurrence Network (3D)',
        scene: {
            xaxis: { showgrid: false, showticklabels: false, title: '' },
            yaxis: { showgrid: false, showticklabels: false, title: '' },
            zaxis: { showgrid: false, showticklabels: false, title: '' }
        },
        height: 500,
        showlegend: false
    };
    
    Plotly.newPlot(elementId, traces, layout, { responsive: true });
}

// Create 3D Bar Chart
function create3DBarChart(data, elementId) {
    const trace = {
        x: data.x,
        y: data.y,
        z: data.z,
        type: 'bar3d',
        colorscale: 'Plasma',
        colorbar: { title: 'Percentage %' },
        hovertemplate: 'Age: %{x}<br>Skin Type: %{y}<br>Usage: %{z}%<extra></extra>'
    };
    
    const layout = {
        title: 'Skin Type Distribution by Age Group (3D)',
        scene: {
            xaxis: { title: 'Age Group' },
            yaxis: { title: 'Skin Type' },
            zaxis: { title: 'Percentage (%)' }
        },
        height: 500,
        margin: { l: 0, r: 0, b: 0, t: 50 }
    };
    
    Plotly.newPlot(elementId, [trace], layout, { responsive: true });
}

// Create Heatmap
function createHeatmap(data, elementId) {
    const trace = {
        z: data.values,
        x: data.xLabels,
        y: data.yLabels,
        type: 'heatmap',
        colorscale: 'Viridis',
        colorbar: { title: 'Usage %' },
        hovertemplate: 'Ingredient: %{x}<br>Age Group: %{y}<br>Usage: %{z}%<extra></extra>'
    };
    
    const layout = {
        title: 'Active Ingredients Usage by Age Group',
        xaxis: { title: 'Ingredients', tickangle: -45 },
        yaxis: { title: 'Age Group' },
        height: 400
    };
    
    Plotly.newPlot(elementId, [trace], layout, { responsive: true });
}

// Sample data generator for demonstration
function generateSampleData() {
    // Sample nodes for network graph
    const ingredients = ['Retinol', 'Vitamin C', 'Niacinamide', 'HA', 'Salicylic Acid', 'Ceramides'];
    const nodes = ingredients.map((name, i) => ({
        name: name,
        x: Math.random() * 10,
        y: Math.random() * 10,
        z: Math.random() * 10,
        size: 15,
        color: '#667eea'
    }));
    
    const edges = [];
    for (let i = 0; i < nodes.length - 1; i++) {
        edges.push({ from: i, to: i + 1 });
    }
    
    // Sample surface data
    const surfaceZ = Array(10).fill().map(() => Array(10).fill().map(() => Math.random() * 100));
    const surfaceX = Array(10).fill().map((_, i) => `$${i * 50}-${(i + 1) * 50}`);
    const surfaceY = Array(10).fill().map((_, i) => `${20 + i * 5}-${25 + i * 5}`);
    
    // Sample bar chart data
    const skinTypes = ['Oily', 'Dry', 'Combination', 'Normal', 'Sensitive'];
    const ageGroups = ['18-25', '26-35', '36-45', '46-55', '55+'];
    const barZ = skinTypes.map(() => ageGroups.map(() => Math.random() * 100));
    
    // Sample heatmap data
    const heatmapValues = [
        [45, 65, 78, 65, 45, 30],
        [55, 75, 85, 75, 55, 45],
        [65, 85, 75, 85, 65, 60],
        [75, 80, 65, 80, 70, 70],
        [80, 70, 55, 70, 65, 75]
    ];
    
    return {
        nodes, edges,
        surfaceZ, surfaceX, surfaceY,
        barZ, skinTypes, ageGroups,
        heatmapValues
    };
}

// Export functions for use in dashboard
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        create3DScatterPlot,
        create3DSurfacePlot,
        create3DNetworkGraph,
        create3DBarChart,
        createHeatmap,
        generateSampleData
    };
}