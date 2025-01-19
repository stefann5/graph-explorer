from sok.graph.explorer.api.model.graph import Graph
from sok.graph.explorer.api.services.graph import DataVisualizerBase


class SimpleVisualizer(DataVisualizerBase):
    def identifier(self):
        return "SimpleVisualizer"

    def name(self):
        return "Simple graph visualizer"
    
    def visualize_graph(self, graph: Graph):
        return self.sw_str(graph)

    def nodes_sw(self, graph: Graph) -> str:
        string = "{"
        for node_id in graph.nodes:
            string = string + node_id + \
                     ':' '{' + "\"id\":" + f"\"{node_id}\"" + '},'
        string = string + '}'

        return str(string)

    def links_sw(self, graph: Graph) -> str:
        string = '['
        for edge in graph.edges:
            string = string + '{' + "\"source\":" + \
                     "\"" + str(edge.source) + "\"" + ',' + "\"target\":" + \
                     "\"" + str(edge.target) + "\"" + '},'
        string = string + ']'
        return string

    def sw_str(self, graph: Graph) -> str:
        string = "let nodes = " + self.nodes_sw(graph) + "\n"
        string = string + "let links = " + self.links_sw(graph) + "\n"
        string = string + """
            links.forEach(function(link) {
                link.source = nodes[link.source];
                link.target = nodes[link.target];
            });
            
            var force = d3.layout.force()
                .size([400, 400])
                .nodes(d3.values(nodes)) 
                .links(links) 
                .on("tick", tick) 
                .linkDistance(300)
                .charge(-100)
                .start(); 
                
            #treba u okviru base temlate-a napraviti <div id="graph">{% block content %} {% endblock %}</div>    
            
            var svg = d3.select("#graph").select("svg")
                .call(d3.behavior.zoom().on("zoom", function () {
                svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
                }))
                .append("g");
                
                         
            var link = svg.selectAll('.link')
                .data(links)
                .enter().append('line')
                .attr('class', 'link');  
                
            var node = svg.selectAll('.node')
                .data(force.nodes()) //add
                .enter().append('g')
                .attr('class', 'node')
                .attr('id', function(d){return d.name;})
                .on('click',function(){
                   nodeClick(this);
                });  
            
            function nodeClick(el) {
              alert("ID: " + el.id);
            }    
            
            d3.selectAll('.node').each(function(d){simpleView(d);});
            
            function makeSimpleView(d) {
              let width = 150;
              let height = 50;
              let textSize = 10;
    
              d3.select("g#" + d.id)
                .append("rect") 
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", width)
                .attr("height", height)
                .attr("class","node");
    
    
              d3.select("g#" + d.id)
                .append("text")
                .attr("x", width / 2)
                .attr("y", 10)
                .attr("font-size", textSize)
                .attr('font-family','sans-serif')
                .attr('fill','green')
                .attr("class","name")
                .text(d.id);
    
              d3.select("g#" + d.id)
                .append("line")
                .attr('x1',0)
                .attr('y1',textSize)
                .attr('x2',width)
                .attr('y2',textSize)
                .attr('stroke','gray')
                .attr('stroke-width',2);
            }
  
        function tick(e) {

            // node translation
            node.attr("transform", function(d) {
                return "translate(" + d.x + "," + d.y + ")";
            })
            .call(force.drag);
    
            // edge correction
            link.attr('x1', function(d) { return d.source.x; })
                .attr('y1', function(d) { return d.source.y; })
                .attr('x2', function(d) { return d.target.x; })
                .attr('y2', function(d) { return d.target.y; });
                
            updateMiniMap()    
        }
        initializeMiniMap(links, force)
        """


