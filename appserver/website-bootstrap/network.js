const network_svg_id= "network-svg";

$(document).ready(function(){

    document.getElementById('update-graph-btn').addEventListener('click', function () {
        // example URL /retweeters?username=Drake&count=20
        const svgPresent = !! document.getElementById(network_svg_id);
        if (svgPresent) { d3.select("#" + network_svg_id).remove(); }
        let retweetNetworkURL = 'http://18.214.197.203:5000/retweeters?username=';
        let uname = document.getElementById('search-network').value;
        let retweets = document.getElementById('drop-list-network').value;
        let networkData = {};
        let nodes = [];
        let links = [];
        if (!uname || uname === ''){
            alert("Must enter a Username!")
        } else {
            let rootnode = {};
            rootnode.id = uname;
            nodes.push(rootnode);
            alert(JSON.stringify(nodes));
            retweetNetworkURL += uname + '&count=' + retweets;
            // alert(retweetNetworkURL); // check that the url is correct
            $.getJSON(retweetNetworkURL, function(data){
                let network = data;
                // alert(JSON.stringify(network)); // check that network data is returned
                let i = 0;
                for(i; i < retweets.valueOf(); i++){
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
                alert(JSON.stringify(networkData)); // check that data was correctly parsed
                graphNetwork(networkData)
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
            {"source": "n1", "target": "n12", "value": 3},
            {"source": "n1", "target": "n13", "value": 2},
            {"source": "n1", "target": "n11", "value": 30},
            {"source": "n13", "target": "n2", "value": 1},
            {"source": "n15", "target": "n2", "value": 12},
            {"source": "n4", "target": "n20", "value": 1},
            {"source": "n17", "target": "n2", "value": 10},
            {"source": "n18", "target": "n20", "value": 1},
            {"source": "n19", "target": "n12", "value": 1},
            {"source": "n19", "target": "n9", "value": 1},
            {"source": "n11", "target": "n17", "value": 19},
            {"source": "n9", "target": "n20", "value": 1},
            {"source": "n17", "target": "n5", "value": 11},
            {"source": "n1", "target": "n14", "value": 3},
            {"source": "n1", "target": "n15", "value": 7},
            {"source": "n1", "target": "n16", "value": 12},
            {"source": "n2", "target": "n4", "value": 7},
            {"source": "n3", "target": "n5", "value": 9},
            {"source": "n2", "target": "n10", "value": 7},
            {"source": "n3", "target": "n9", "value": 7},
            {"source": "n4", "target": "n8", "value": 20},
            {"source": "n4", "target": "n7", "value": 15},
            {"source": "n8", "target": "n1", "value": 1},
            {"source": "n6", "target": "n1", "value": 1}
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
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody()
                .strength(-300)
                .theta(0.8)
                .distanceMax(150)
        )
        .force("center", d3.forceCenter(width / 2, height / 2));

    let link = svg.append("g")
        .style("stroke", "#224cb5")
        .selectAll("line")
        .data(data.links)
        .enter()
        .append("line")
        .style("stroke-width", function(d) {return Math.sqrt(d.value);});

    let node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(data.nodes)
        .enter()
        .append("circle")
        //.attr("r", 4)
        .call(d3.drag(simulation)
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

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
            .attr("r", 17)
            .style("fill", "#ffffff")
            .style("stroke", "#000000")
            .style("stroke-width", "1px")
            .attr("cx", function (d) { return d.x+5; })
            .attr("cy", function(d) { return d.y-3; });
        label
            .attr("x", function(d) { return d.x; })
            .attr("y", function (d) { return d.y; })
            .style("font-size", "12px").style("fill", "#000000");
    }
}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
    //below code doesn't retract after drag
    //d.fx = d3.event.x
    //d.fy = d3.event.y
    //if (!d3.event.active) simulation.alphaTarget(0);
}