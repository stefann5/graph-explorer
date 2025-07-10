from datetime import datetime
from sok.graph.explorer.api.model.graph import Graph
from sok.graph.explorer.api.services.graph import DataVisualizerBase
import json

class SimpleVisualizer(DataVisualizerBase):
    def identifier(self):
        return "SimpleVisualizer"

    def name(self):
        return "Simple graph visualizer"
    
    def visualize_graph(self, graph: Graph):
        return self.sw_str(graph)

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

    def links_sw(self, graph: Graph) -> str:
        links_list = []
        for edge in graph.edges:
            links_list.append({
                "source": str(edge.source),
                "target": str(edge.target)
            })
        return json.dumps(links_list)

    def sw_str(self, graph: Graph) -> str:
        nodes_json = self.nodes_sw(graph)
        links_json = self.links_sw(graph)
        
        js_code = f"""
       
        
            var nodes = {nodes_json};
var links = {links_json};

links.forEach(function(link) {{
    link.source = nodes[link.source];
    link.target = nodes[link.target];
}});

// Create main view with zoom container
createGraphView(".main-view", 1200, 750, true);


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

    var force = d3.layout.force()
        .size([width, height])
        .nodes(d3.values(nodes))
        .links(links)
        .on("tick", tick)
        .linkDistance(container === ".bird-view" ? 200 : 400)
        .charge(container === ".bird-view" ? -1000 : -3000)
        .gravity(0.1)
        .start();

    

    function collide(node) {{
        var r = 100,
            nx1 = node.x - r,
            nx2 = node.x + r,
            ny1 = node.y - r,
            ny2 = node.y + r;
        return function(quad, x1, y1, x2, y2) {{
            if (quad.point && (quad.point !== node)) {{
                var x = node.x - quad.point.x,
                    y = node.y - quad.point.y,
                    l = Math.sqrt(x * x + y * y),
                    r = 200;
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

    var link = g.selectAll('.link')
        .data(force.links())
        .enter().append('path')  // Changed from line to path for curved links
        .attr('class', 'link')
        .style('stroke', '#999')
        .style('stroke-width', '2px')
        .style('fill', 'none');

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
        makeSimpleView(d, container);
    }});
                
   function makeSimpleView(d, container) {{
    let scale = 1;
    let width = 180 * scale;
    let height = 60 * scale;
    let textSize = 12 * scale;
    var gradient = defs.append("linearGradient")
        .attr("id", "node-gradient")
        .attr("x1", "0%")
        .attr("y1", "0%")
        .attr("x2", "0%")
        .attr("y2", "100%");

    gradient.append("stop")
        .attr("offset", "0%")
        .attr("style", "stop-color:#ffffff;stop-opacity:1");

    gradient.append("stop")
        .attr("offset", "100%")
        .attr("style", "stop-color:#f0f0f0;stop-opacity:1");

    let containerId = container.replace('.', '');

    // Select the node group and add click event
    let nodeGroup = d3.select("#" + containerId + "-node-" + d.id)
        .on('click', function(d) {{
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

    // Append the rect without click event
    nodeGroup.append("rect")
        .attr("x", -width / 2)
        .attr("y", -height / 2)
        .attr("rx", 6 * scale)
        .attr("ry", 6 * scale)
        .attr("width", width)
        .attr("height", height)
        .attr("class", "node")
        .style('fill', 'url(#node-gradient)')
        .style('stroke', '#2563eb')
        .style('stroke-width', 2 * scale);

    nodeGroup.append("text")
        .attr("x", 0)
        .attr("y", 0)
        .attr("text-anchor", "middle")
        .attr("dominant-baseline", "middle")
        .attr("font-size", textSize)
        .attr('font-family', 'system-ui, sans-serif')
        .attr('font-weight', '600')
        .attr('fill', '#1e40af')
        .attr("class", "name")
        .text(d.id);

    function updateNodeColor(nodeId, viewName) {{
        let selector = "#" + viewName + "-node-" + nodeId;
        let rect = d3.select(selector).select('rect');
        let isClicked = rect.classed('clicked');

        rect.classed('clicked', !isClicked);
        rect.style('fill', !isClicked ? '#93c5fd' : 'url(#node-gradient)');
    }}
}}

        
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

    
    initializeMiniMap(links, force,makeSimpleView);
}}
        """
        return js_code