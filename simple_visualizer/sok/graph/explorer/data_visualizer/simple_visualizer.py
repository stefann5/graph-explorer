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
            nodes_dict[node_id] = {"id": node_id}
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
            createGraphView(".main-view", 400, 400, true);
            // Create bird view
            
            
            function createGraphView(container, width, height, enableZoom) {{
                d3.select(container).selectAll("svg").remove();
                var svg = d3.select(container)
                    .append("svg")
                    .attr("width", "100%")
                    .attr("height", "100%");

                // Create a group for zoom transformation
                var g = svg.append("g");

                // Define zoom behavior
                if (enableZoom) {{
                    var zoom = d3.behavior.zoom()
                        .scaleExtent([0.1, 10])
                        .on("zoom", function () {{
                            g.attr("transform",
                                "translate(" + d3.event.translate + ")" +
                                " scale(" + d3.event.scale + ")");
                        }});
                    svg.call(zoom);
                }}

                var force = d3.layout.force()
                    .size([width, height])
                    .nodes(d3.values(nodes))
                    .links(links)
                    .on("tick", tick)
                    .linkDistance(container === ".bird-view" ? 150 : 300)
                    .charge(container === ".bird-view" ? -50 : -100)
                    .start();

                var link = g.selectAll('.link')
                    .data(force.links())
                    .enter().append('line')
                    .attr('class', 'link')
                    .style('stroke', '#999')
                    .style('stroke-width', '1px');

                var node = g.selectAll('.node')
                    .data(force.nodes())
                    .enter().append('g')
                    .attr('class', 'node')
                    .attr('id', function (d) {{
                        return container.replace('.', '') + '-node-' + d.id;
                    }})
                    .on('click', nodeClick)
                    .call(d3.behavior.drag()
                .on("dragstart", function(d) {{
                    d3.event.sourceEvent.stopPropagation();
                    if (enableZoom) {{
                        zoom.on("zoom", null);
                    }}
                    d.fixed = true;  // Fix this specific node
                    force.resume();  // Keep the simulation running
                }})
                .on("drag", function(d) {{
                    d.px += d3.event.dx;
                    d.py += d3.event.dy;
                    d.x += d3.event.dx;
                    d.y += d3.event.dy;
                    force.resume();  // Keep the simulation running
                }})
                .on("dragend", function(d) {{
                    if (enableZoom) {{
                        zoom.on("zoom", function() {{
                            g.attr("transform",
                                "translate(" + d3.event.translate + ")" +
                                " scale(" + d3.event.scale + ")");
                        }});
                    }}
                    // Keep d.fixed = true to prevent the node from moving
                    d.fixed = false;
                    force.resume();  // Keep the simulation running
                }}));

                function nodeClick(d) {{
                    alert("ID: " + d.id);
                }}

                force.nodes().forEach(function (d) {{
                    makeSimpleView(d, container);
                }});
                            
                function makeSimpleView(d, container) {{
                    let scale = container === ".bird-view" ? 0.5 : 1;
                    let width = 150 * scale;
                    let height = 50 * scale;
                    let textSize = 10 * scale;
                    
                    let containerId = container.replace('.', '');
                    
                    d3.select("#" + containerId + "-node-" + d.id)
                        .append("rect")
                        .attr("x", 0)
                        .attr("y", 0)
                        .attr("width", width)
                        .attr("height", height)
                        .attr("class", "node")
                        .style('fill', '#fff')
                        .style('stroke', '#000');
                    
                    d3.select("#" + containerId + "-node-" + d.id)
                        .append("text")
                        .attr("x", width / 2)
                        .attr("y", 10 * scale)
                        .attr("font-size", textSize)
                        .attr('font-family', 'sans-serif')
                        .attr('fill', 'green')
                        .attr("class", "name")
                        .text(d.id);
                    
                    d3.select("#" + containerId + "-node-" + d.id)
                        .append("line")
                        .attr('x1', 0)
                        .attr('y1', textSize)
                        .attr('x2', width)
                        .attr('y2', textSize)
                        .attr('stroke', 'gray')
                        .attr('stroke-width', 2 * scale);
                }}
                    
                function tick() {{
                    node.attr("transform", function(d) {{
                        return "translate(" + d.x + "," + d.y + ")";
                    }});
                    
                    link.attr('x1', function(d) {{ return d.source.x; }})
                        .attr('y1', function(d) {{ return d.source.y; }})
                        .attr('x2', function(d) {{ return d.target.x; }})
                        .attr('y2', function(d) {{ return d.target.y; }});
                    updateMiniMap();
                }}
                initializeMiniMap(links,force);
            }}
        
        """
        return js_code
    