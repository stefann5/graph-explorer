from sok.graph.explorer.api.model.graph import Graph
from sok.graph.explorer.api.services.graph import DataVisualizerBase
import json
from datetime import datetime

class BlockVisualizer(DataVisualizerBase):
    def identifier(self):
        return "BlockVisualizer"

    def name(self):
        return "Block graph visualizer"
    
    def visualize_graph(self, graph: Graph):
        return self.sw_str(graph)
    
    #Takes graph nodes and converts them into dictionary
    #It returns JSON string of all nodes with their attributes
    def nodes_sw(self, graph: Graph) -> str:
        nodes_dict = {}
        for node_id in graph.nodes:
            attributes = graph.nodes[node_id].data["attributes"]
            # Create a new dictionary with converted datetime values
            converted_attributes = {}
            
            for key, value in attributes.items():
                if isinstance(value, datetime):
                    converted_attributes[key] = value.isoformat()
                else:
                    converted_attributes[key] = value
                    
            nodes_dict[node_id] = {
                "id": node_id,
                "attributes": converted_attributes
            }
        return json.dumps(nodes_dict)

    #Converts graph edges to JSON format
    def links_sw(self, graph: Graph) -> str:
        links_list = []
        for edge in graph.edges:
            links_list.append({
                "source": str(edge.source),
                "target": str(edge.target)
            })
        return json.dumps(links_list)
    
    #Generates all neccessary JavaScript code
    def sw_str(self, graph: Graph) -> str:
        nodes_json = self.nodes_sw(graph)
        links_json = self.links_sw(graph)
        
        js_code = f"""
            var nodes = {nodes_json};
            var links = {links_json};

            //Converts all link references from IDs to node objects
            links.forEach(function(link) {{
                link.source = nodes[link.source];
                link.target = nodes[link.target];
            }});

            // Create main view with zoom container
            createGraphView(".main-view", 1200, 750, true);

            // Function to calculate text width
            function getTextWidth(text, fontSize, fontFamily) {{
                var canvas = document.createElement("canvas");
                var context = canvas.getContext("2d");
                context.font = fontSize + "px " + fontFamily;
                return context.measureText(text).width;
            }}

            function createGraphView(container, width, height, enableZoom) {{
                d3.select(container).selectAll("svg").remove();
                var svg = d3.select(container)
                    .append("svg")
                    .attr("width", "100%")
                    .attr("height", "100%")
                    .attr("class", "graph-svg");
                var tooltip = d3.select("body")
                    .append("div")
                    .attr("class", "tooltip")
                    .style("opacity", 0);

                // Add definitions for gradients and filters
                var defs = svg.append("defs");
    
                // Add drop shadow filter
                var filter = defs.append("filter")
                    .attr("id", "drop-shadow")
                    .attr("height", "130%");

                filter.append("feGaussianBlur")
                    .attr("in", "SourceAlpha")
                    .attr("stdDeviation", 3)
                    .attr("result", "blur");

                filter.append("feOffset")
                    .attr("in", "blur")
                    .attr("dx", 2)
                    .attr("dy", 2)
                    .attr("result", "offsetBlur");

                var feMerge = filter.append("feMerge");
                feMerge.append("feMergeNode")
                    .attr("in", "offsetBlur");
                feMerge.append("feMergeNode")
                    .attr("in", "SourceGraphic");

                // Add gradient
                // Create a group for zoom transformation
                var g = svg.append("g");

                // Define zoom behavior
                if (enableZoom) {{
                    var zoom = d3.behavior.zoom()
                        .scaleExtent([0.1, 10])
                        .on("zoom", function () {{
                            const transform = {{
                                x: d3.event.translate[0],
                                y: d3.event.translate[1],
                                k: d3.event.scale,
                            }};

                            g.attr("transform", 
                                "translate(" + transform.x + "," + transform.y + ")" +
                                " scale(" + transform.k + ")"
                            );

                            updateViewport(transform, width, height);
                        }});
                    svg.call(zoom);
                }}

                //Force Layout Configuration - creates simulation that positions nodes automatically
                var force = d3.layout.force()
                    .size([width, height])
                    .nodes(d3.values(nodes))
                    .links(links)
                    .on("tick", tick)
                    .linkDistance(container === ".bird-view" ? 250 : 500)
                    .charge(container === ".bird-view" ? -1500 : -4000)
                    .gravity(0.1)
                    .start();

                //Collision Detection - prevents nodes from overlapping
                function collide(node) {{
                    var r = node.width ? node.width / 2 + 20 : 120,
                        nx1 = node.x - r,
                        nx2 = node.x + r,
                        ny1 = node.y - r,
                        ny2 = node.y + r;
                    return function(quad, x1, y1, x2, y2) {{
                        if (quad.point && (quad.point !== node)) {{
                            var x = node.x - quad.point.x,
                                y = node.y - quad.point.y,
                                l = Math.sqrt(x * x + y * y),
                                r = (node.width || 240) / 2 + (quad.point.width || 240) / 2 + 40;
                            if (l < r) {{
                                l = (l - r) / l * 0.5;
                                node.x -= x *= l;
                                node.y -= y *= l;
                                quad.point.x += x;
                                quad.point.y += y;
                            }}
                        }}
                        return x1 > nx2 || x2 < nx1 || y1 > ny2 || y2 < ny1;
                    }};
                }}

                //Creates curved lines connectiong related nodes
                var link = g.selectAll('.link')
                    .data(force.links())
                    .enter().append('path')  // Changed from line to path for curved links
                    .attr('class', 'link')
                    .style('stroke', '#999')
                    .style('stroke-width', '2px')
                    .style('fill', 'none');

                //Creates interactive node groups - adds hover effects and enables dragging nodes around
                var node = g.selectAll('.node')
                    .data(force.nodes())
                    .enter().append('g')
                    .attr('class', 'node')
                    .attr('id', function (d) {{
                        return container.replace('.', '') + '-node-' + d.id;
                    }}) 
                .on('mouseover', function(d) {{
                    // Show tooltip with attributes
                    tooltip.transition()
                        .duration(200)
                        .style("opacity", .9);
                    
                    let tooltipContent = "<div style='font-weight:bold;margin-bottom:5px;'>" + d.id + "</div>";
                    for (let key in d.attributes) {{
                        tooltipContent += "<div><strong>" + key + ":</strong> " + d.attributes[key] + "</div>";
                    }}
                    
                    tooltip.html(tooltipContent)
                        .style("left", (d3.event.pageX + 10) + "px")
                        .style("top", (d3.event.pageY - 10) + "px");

                    // Node hover effect
                    d3.select(this).select('rect')
                        .transition()
                        .duration(300)
                        .style('filter', 'url(#drop-shadow)')
                        .style('transform', 'scale(1.05)');
                }})
                .on('mouseout', function(d) {{
                    // Hide tooltip
                    tooltip.transition()
                        .duration(500)
                        .style("opacity", 0);

                    // Remove hover effect if not clicked
                    let rect = d3.select(this).select('rect');
                    if (!rect.classed('clicked')) {{
                        rect.transition()
                            .duration(300)
                            .style('filter', null)
                            .style('transform', 'scale(1)');
                    }}
                }})
                .call(d3.behavior.drag()
                    .on("dragstart", function(d) {{
                        d3.event.sourceEvent.stopPropagation();
                        if (enableZoom) {{
                            zoom.on("zoom", null);
                        }}
                        d.fixed = true;
                        force.resume();
                    }})
                .on("drag", function(d) {{
                    d.px += d3.event.dx;
                    d.py += d3.event.dy;
                    d.x += d3.event.dx;
                    d.y += d3.event.dy;
                    force.resume();
                }})
                .on("dragend", function(d) {{
                    if (enableZoom) {{
                        zoom.on("zoom", function() {{
                            const transform = {{
                            x: d3.event.translate[0],
                            y: d3.event.translate[1],
                            k: d3.event.scale,
                        }};

                        g.attr("transform", 
                            "translate(" + transform.x + "," + transform.y + ")" +
                            " scale(" + transform.k + ")"
                        );

                        updateViewport(transform, width, height);
                        }});
                    }}
                    d.fixed = false;
                    force.resume();
                }}));

                function nodeClick(d) {{
                    // Node click handler
                }}

                force.nodes().forEach(function (d) {{
                    makeBlockView(d, container);
                }});
                
                //Block Node Rendering
                function makeBlockView(d, container) {{
                    let scale = 1;
    
                    // Calculate dynamic size based on content
                    let attributes = d.attributes;
                    let numAttributes = Object.keys(attributes).length;
                    let baseHeight = 40;
                    let attributeHeight = 20;
                    let padding = 20;
                    
                    // Calculate required width based on content
                    let fontFamily = "system-ui, sans-serif";
                    let titleSize = 13 * scale;
                    let textSize = 11 * scale;
                    
                    // Minimum width for the node ID (title)
                    let titleWidth = getTextWidth(d.id, titleSize, fontFamily) + 40;
                    
                    // Calculate width needed for attributes - use fixed layout approach
                    let maxKeyWidth = 0;
                    let maxValueWidth = 0;
                    
                    for (let key in attributes) {{
                        let value = attributes[key];
                        let displayValue = value;
                        
                        // Truncate long values for display
                        if (typeof value === 'string' && value.length > 35) {{
                            displayValue = value.substring(0, 35) + '...';
                        }}
                        
                        let keyWidth = getTextWidth(key + ":", textSize, fontFamily);
                        let valueWidth = getTextWidth(displayValue, textSize, fontFamily);
                        
                        if (keyWidth > maxKeyWidth) {{
                            maxKeyWidth = keyWidth;
                        }}
                        if (valueWidth > maxValueWidth) {{
                            maxValueWidth = valueWidth;
                        }}
                    }}
                    
                    // Calculate total width: left margin + max key width + spacing + max value width + right margin
                    let calculatedWidth = 20 + Math.max(maxKeyWidth, 80) + 10 + maxValueWidth + 20;
                    
                    // Use the maximum of title width and calculated width, with minimum of 220px
                    let width = Math.max(titleWidth, calculatedWidth, 220) * scale;
                    let height = (baseHeight + numAttributes * attributeHeight + padding * 2) * scale;
                    let headerHeight = 30 * scale;
                    
                    // Store width in node data for collision detection
                    d.width = width;
                    d.height = height;

                    var gradient = defs.append("linearGradient")
                        .attr("id", "block-gradient-" + d.id)
                        .attr("x1", "0%")
                        .attr("y1", "0%")
                        .attr("x2", "0%")
                        .attr("y2", "100%");

                    gradient.append("stop")
                        .attr("offset", "0%")
                        .attr("style", "stop-color:#f8fafc;stop-opacity:1");

                    gradient.append("stop")
                        .attr("offset", "100%")
                        .attr("style", "stop-color:#e2e8f0;stop-opacity:1");

                    var headerGradient = defs.append("linearGradient")
                        .attr("id", "header-gradient-" + d.id)
                        .attr("x1", "0%")
                        .attr("y1", "0%")
                        .attr("x2", "0%")
                        .attr("y2", "100%");

                    headerGradient.append("stop")
                        .attr("offset", "0%")
                        .attr("style", "stop-color:#3b82f6;stop-opacity:1");

                    headerGradient.append("stop")
                        .attr("offset", "100%")
                        .attr("style", "stop-color:#1e40af;stop-opacity:1");

                    let containerId = container.replace('.', '');

                    // Select the node group and add click event
                    let nodeGroup = d3.select("#" + containerId + "-node-" + d.id).on('click', function(d) {{
                        // Fix the node position
                        if (typeof d.fx == 'undefined'||d.fx==null){{
                            d.fx = d.x;
                            d.fy = d.y;
                        }}
                        else{{
                            d.fx=null;
                            d.fy=null;
                        }}

                        // Highlight the clicked node
                        updateNodeColor(d.id, 'main-view');
                        updateNodeColor(d.id, 'bird-view');
                    }});

                    // Main container rectangle
                    nodeGroup.append("rect")
                        .attr("x", -width / 2)
                        .attr("y", -height / 2)
                        .attr("rx", 8 * scale)
                        .attr("ry", 8 * scale)
                        .attr("width", width)
                        .attr("height", height)
                        .attr("class", "node-container")
                        .style('fill', 'url(#block-gradient-' + d.id + ')')
                        .style('stroke', '#cbd5e1')
                        .style('stroke-width', 1 * scale);

                    // Header rectangle
                    nodeGroup.append("rect")
                        .attr("x", -width / 2)
                        .attr("y", -height / 2)
                        .attr("rx", 8 * scale)
                        .attr("ry", 8 * scale)
                        .attr("width", width)
                        .attr("height", headerHeight)
                        .attr("class", "node-header")
                        .style('fill', 'url(#header-gradient-' + d.id + ')')
                        .style('stroke', '#1e40af')
                        .style('stroke-width', 1 * scale);

                    // Header rectangle bottom (to square off the bottom corners)
                    nodeGroup.append("rect")
                        .attr("x", -width / 2)
                        .attr("y", -height / 2 + headerHeight - 5)
                        .attr("width", width)
                        .attr("height", 5)
                        .style('fill', 'url(#header-gradient-' + d.id + ')')
                        .style('stroke', 'none');

                    // Title text (node ID)
                    nodeGroup.append("text")
                        .attr("x", 0)
                        .attr("y", -height / 2 + headerHeight / 2)
                        .attr("text-anchor", "middle")
                        .attr("dominant-baseline", "middle")
                        .attr("font-size", titleSize)
                        .attr('font-family', 'system-ui, sans-serif')
                        .attr('font-weight', '700')
                        .attr('fill', 'white')
                        .attr("class", "node-title")
                        .text(d.id);

                    // Add attributes text
                    let yOffset = headerHeight + 15;
                    let attributeKeys = Object.keys(attributes);
                    let leftMargin = 30;
                    let keyValueSpacing = 5;
    
                    attributeKeys.forEach(function(key, index) {{
                        let value = attributes[key];
                        let displayValue = value;
                    
                        // Truncate long values
                        if (typeof value === 'string' && value.length > 35) {{
                            displayValue = value.substring(0, 35) + '...';
                        }}
        
                        let yPosition = -height / 2 + yOffset + index * attributeHeight;
                        
                        // Attribute key
                        nodeGroup.append("text")
                            .attr("x", -width / 2 + leftMargin)
                            .attr("y", yPosition)
                            .attr("text-anchor", "start")
                            .attr("dominant-baseline", "middle")
                            .attr("font-size", textSize)
                            .attr('font-family', 'system-ui, sans-serif')
                            .attr('font-weight', '600')
                            .attr('fill', '#374151')
                            .attr("class", "attribute-key")
                            .text(key + ":");

                        // Attribute value - fixed position from left margin
                        nodeGroup.append("text")
                            .attr("x", -width / 2 + leftMargin + 80)
                            .attr("y", yPosition)
                            .attr("text-anchor", "start")
                            .attr("dominant-baseline", "middle")
                            .attr("font-size", textSize)
                            .attr('font-family', 'system-ui, sans-serif')
                            .attr('font-weight', '400')
                            .attr('fill', '#6b7280')
                            .attr("class", "attribute-value")
                            .text(displayValue);
                    }});

                    function updateNodeColor(nodeId, viewName) {{
                        let selector = "#" + viewName + "-node-" + nodeId;
                        let container = d3.select(selector).select('.node-container');
                        let header = d3.select(selector).select('.node-header');
                        let isClicked = container.classed('clicked');

                        container.classed('clicked', !isClicked);
                        header.classed('clicked', !isClicked);
            
                        if (!isClicked) {{
                            container.style('fill', '#fef3c7');
                            header.style('fill', '#f59e0b');
                        }} else {{
                            container.style('fill', 'url(#block-gradient-' + nodeId + ')');
                            header.style('fill', 'url(#header-gradient-' + nodeId + ')');
                        }}
                    }}
                }}

                //Animation and updates
                function tick() {{
                    node.attr("transform", function(d) {{
                        // Ensure fixed nodes don't move
                        if (d.fx !== undefined && d.fx != null) {{
                            d.x = d.fx;
                            d.y = d.fy;
                        }}
                        return "translate(" + d.x + "," + d.y + ")";
                    }});

                    // Apply collision only to nodes not being dragged
                    var q = d3.geom.quadtree(force.nodes());
                    force.nodes().forEach(function(node) {{
                        if (!node.dragging) {{ // Skip collision for dragged nodes
                            q.visit(collide(node));
                        }}
                    }});

                    // Update links with curved paths
                    link.attr('d', function(d) {{
                        var dx = d.target.x - d.source.x,
                            dy = d.target.y - d.source.y,
                            dr = Math.sqrt(dx * dx + dy * dy);
                        return "M" + d.source.x + "," + d.source.y +
                            "A" + dr + "," + dr + " 0 0,1 " +
                            d.target.x + "," + d.target.y;
                    }});

                    updateMiniMap();
                }}

                initializeMiniMap(links, force, makeBlockView);
            }}
        """
        return js_code