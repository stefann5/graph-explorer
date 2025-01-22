function initializeMiniMap(links, force) {
    // Reset the mini-map
    d3.select("#bird-view").selectAll("svg").remove();
    
    // Create SVG container for bird view
    var birdViewSvg = d3.select("#bird-view")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%");

    // Create group for the mini-map
    var miniMap = birdViewSvg.append("g")
        .attr("id", "mini-map");

    // Add viewport rectangle
    var viewport = birdViewSvg.append("rect")
        .attr("class", "viewport")
        .attr("fill", "none")
        .attr("stroke", "#2563eb")
        .attr("stroke-width", "2px")
        .attr("pointer-events", "none")
        .style("opacity", 0.3);

    // Initialize mini-map elements
    var miniMapLinks = miniMap.selectAll(".link")
        .data(links)
        .enter()
        .append("path")
        .attr("class", "link")
        .style("stroke", "#999")
        .style("stroke-width", "1px")
        .style("fill", "none");

    var miniMapNodes = miniMap.selectAll(".node")
        .data(force.nodes())
        .enter()
        .append("g")
        .attr("class", "node");

    // Initialize nodes with the same styling as main view
    force.nodes().forEach(function(d) {
        makeSimpleView(d, ".bird-view");
    });

    // Update function for mini-map
    function updateMiniMap() {
        // Update links with curved paths
        miniMapLinks.attr('d', function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" + d.source.x + "," + d.source.y + 
                   "A" + dr + "," + dr + " 0 0,1 " + 
                   d.target.x + "," + d.target.y;
        });

        // Update node positions
        miniMapNodes.attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

        updateViewport();
    }

    // Function to calculate and update viewport position
    function updateViewport() {
        // Get the current transform of the main view
        var transform = d3.transform(d3.select(".main-view g").attr("transform"));
        var scale = transform.scale[0];
        var translate = transform.translate;

        // Get the dimensions of both views
        var mainViewDims = getDimensions(".main-view");
        var birdViewDims = getDimensions("#bird-view");
        
        // Get the bounds of all nodes
        var bounds = getGraphBounds();
        
        // Calculate the scale factor for the bird view
        var birdViewScale = Math.min(
            birdViewDims.width / (bounds.maxX - bounds.minX),
            birdViewDims.height / (bounds.maxY - bounds.minY)
        ) * 0.9; // 90% to add margin

        // Calculate the viewport dimensions
        var viewportWidth = mainViewDims.width / scale;
        var viewportHeight = mainViewDims.height / scale;

        // Calculate the viewport position
        var vpX = (-translate[0] / scale) * birdViewScale;
        var vpY = (-translate[1] / scale) * birdViewScale;

        // Update viewport rectangle
        viewport
            .attr("x", vpX)
            .attr("y", vpY)
            .attr("width", viewportWidth * birdViewScale)
            .attr("height", viewportHeight * birdViewScale);

        // Scale and position the mini-map
        var translateX = (birdViewDims.width - (bounds.maxX - bounds.minX) * birdViewScale) / 2 - bounds.minX * birdViewScale;
        var translateY = (birdViewDims.height - (bounds.maxY - bounds.minY) * birdViewScale) / 2 - bounds.minY * birdViewScale;

        miniMap.attr("transform", `translate(${translateX}, ${translateY}) scale(${birdViewScale})`);
    }

    // Function to get graph bounds
    function getGraphBounds() {
        var nodes = force.nodes();
        var bounds = {
            minX: Infinity,
            minY: Infinity,
            maxX: -Infinity,
            maxY: -Infinity
        };

        nodes.forEach(function(node) {
            bounds.minX = Math.min(bounds.minX, node.x);
            bounds.minY = Math.min(bounds.minY, node.y);
            bounds.maxX = Math.max(bounds.maxX, node.x);
            bounds.maxY = Math.max(bounds.maxY, node.y);
        });

        return bounds;
    }

    // Add zoom event listener to main view
    d3.select(".main-view svg").select("g")
        .on("mousedown.zoom", function() {
            updateViewport();
        })
        .on("mousemove.zoom", function() {
            if (d3.event.which === 1) { // Left mouse button
                updateViewport();
            }
        })
        .on("mouseup.zoom", function() {
            updateViewport();
        });

    // Initial positioning of the mini-map
    force.on("end", function() {
        updateViewport();
    });

    return {
        update: updateMiniMap,
        updateViewport: updateViewport
    };
}