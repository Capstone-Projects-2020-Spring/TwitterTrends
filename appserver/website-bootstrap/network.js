const network_svg_id= "network-svg";

$(document).ready(function(){

    document.getElementById('update-graph-btn').addEventListener('click', function () {
        // example URL /retweeters?username=Drake&count=20
        const svgPresent = !! document.getElementById(network_svg_id);
        if (svgPresent) { d3.select("#" + network_svg_id).remove(); }
        let retweetNetworkURL = 'http://18.214.197.203:5000/retweeters?username=';
        let uname = document.getElementById('search-network').value;
        let retweeter_count = document.getElementById('drop-list-network').value;
        let networkData = {};
        let nodes = [];
        let links = [];
        if (!uname || uname === ''){
            alert("Must enter a Username!")
        } else {
            let rootnode = {};
            rootnode.id = uname;
            nodes.push(rootnode);
            // alert(JSON.stringify(nodes));
            retweetNetworkURL += uname + '&count=' + retweeter_count;
            // alert(retweetNetworkURL); // check that the url is correct
            $.getJSON(retweetNetworkURL, function(data){
                let network = data;
                // alert(JSON.stringify(network)); // check that network data is returned
                let i = 0;
                for(i; i < retweeter_count.valueOf(); i++){
                    let node = {};
                    let link = {};
                    node.id = network[i].username;
                    nodes.push(node);
                    link.source = uname;
                    link.target = network[i].username;
                    link.value = network[i].retweet_count;
                    links.push(link);
                }
                networkData.nodes = nodes;
                networkData.links = links;
                // alert(JSON.stringify(networkData)); // check that data was correctly parsed
                graphNetwork(networkData)
            }).fail(function () {//todo add arguments for the error message
                alert("failed to fetch data about the " + retweeter_count + " retweeters of user " + uname);
            });
        }
    });

    const graphData = {
        "nodes": [
            {"id": "n1"},
            {"id": "n2"},
            {"id": "n3"},
            {"id": "n4"},
            {"id": "n5"},
            {"id": "n6"},
            {"id": "n7"},
            {"id": "n8"},
            {"id": "n9"},
            {"id": "n10"},
            {"id": "n11"},
            {"id": "n12"},
            {"id": "n13"},
            {"id": "n14"},
            {"id": "n15"},
            {"id": "n16"},
            {"id": "n17"},
            {"id": "n18"},
            {"id": "n19"},
            {"id": "n20"}
            ],
        "links": [
            {"source": "n1", "target": "n2", "value": 1},
            {"source": "n1", "target": "n3", "value": 3},
            {"source": "n1", "target": "n4", "value": 2},
            {"source": "n1", "target": "n5", "value": 30},
            {"source": "n1", "target": "n6", "value": 12},
            {"source": "n1", "target": "n7", "value": 1},
            {"source": "n1", "target": "n8", "value": 10},
            {"source": "n1", "target": "n9", "value": 1},
            {"source": "n1", "target": "n10", "value": 1},
            {"source": "n1", "target": "n11", "value": 1},
            {"source": "n1", "target": "n12", "value": 19},
            {"source": "n1", "target": "n13", "value": 1},
            {"source": "n1", "target": "n14", "value": 3},
            {"source": "n1", "target": "n15", "value": 7},
            {"source": "n1", "target": "n16", "value": 12},
            {"source": "n1", "target": "n17", "value": 7},
            {"source": "n1", "target": "n18", "value": 9},
            {"source": "n1", "target": "n19", "value": 7},
            {"source": "n1", "target": "n20", "value": 7}
            ]
    };
    graphNetwork(graphData)
});

function graphNetwork(data) {
    const width = 900, height = 600;

    let svg = d3.select("#network")
        .append("svg")
        .attr("id", network_svg_id)
        .attr("width", width)
        .attr("height", height);

    let simulation = d3.forceSimulation()
        .force("x",d3.forceX(width/2).strength(0.2))
		.force("y",d3.forceY(height/2).strength(0.35))
		.force("charge",d3.forceManyBody().strength(-4000))
		.force("link", d3.forceLink().id(d =>  d.id ))
		.force("collide",d3.forceCollide().radius(d => d.r * 10));

    let link = svg.append("g")
        .style("stroke", "#224cb5")
        .selectAll("line")
        .data(data.links)
        .enter()
        .append("line")
        .style("stroke-width", function(d) {return Math.sqrt(d.value);});

		//tooltip stuff
        let Tooltip = d3.select("#network")
            .append("div")
            .style("opacity", 0)
            .attr("class", "tooltip");

        let mouseover = function(d) {
            Tooltip
                .style("opacity", 1)
				.style("z-index", 1);
        };
        let mousemove = function(d) {
            Tooltip
                .html("ID: " + d.id)
                .style("left", (d3.mouse(this)[0]+50) + "px")
                .style("top", (d3.mouse(this)[1]-40) + "px")
        };
        let mouseleave = function(d) {
            Tooltip
                .style("opacity", 0)
				.style("z-index", -1);
        };

    let node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(data.nodes)
        .enter()
        .append("circle")
		.attr("r", 20)
		//if you really felt like ovals
		//.append("ellipse")
		//.attr("cx", 50)
		//.attr("cy", 50)
		//.attr("rx", 50)
		//.attr("ry", 20)
        .style("fill", "#ffffff")
        .style("stroke", "#000000")
        .style("stroke-width", "1px")
		.on("mouseover", mouseover)
            .on("mousemove", mousemove)
            .on("mouseleave", mouseleave);

    let label = svg.append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(data.nodes)
        .enter()
        .append("text")
        .attr("class", "label")
        .text(function(d) { return d.id; });

    simulation
        .nodes(data.nodes)
        .on("tick", ticked);

    simulation.force("link")
        .links(data.links);

    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
        node
            .attr("cx", function (d) { return d.x+5; })
            .attr("cy", function(d) { return d.y; });
        //removing the node labels because they get messy when the labels are long 
		//label
            //.attr("x", function(d) { return d.x-10; })
            //.attr("y", function (d) { return d.y; })
            //.style("font-size", "12px").style("fill", "#000000");

    }
}

//function dragstarted(d) {
  //  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  // d.fx = d.x;
  //  d.fy = d.y;
//}

//function dragged(d) {
    //d.fx = d3.event.x;
   // d.fy = d3.event.y;
//}

//function dragended(d) {
    //if (!d3.event.active) simulation.alphaTarget(0);
    //d.fx = null;
    //d.fy = null;
    //below code doesn't retract after drag
    //d.fx = d3.event.x
    //d.fy = d3.event.y
    //if (!d3.event.active) simulation.alphaTarget(0);
//}