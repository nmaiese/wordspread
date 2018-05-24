function wordCloud(selector, color_range) {

    var fill = d3.scale.category20();
    

    //Construct the word cloud's SVG element
    var svg = d3.select(selector).append("svg")
        .attr("width", $(selector).width())
        .attr("height", 500)
        .append("g")
        .attr("transform", "translate("+$(selector).width()/2+",250)");


    //Draw the word cloud
    function draw(words) {


        var font_value_scale = d3.scale.linear()
        .domain([
            d3.min(words, function(d){return d.value}),
            d3.max(words, function(d){return d.value})])
        .range([20,50]);


        var color_counter_scale = d3.scale.linear()
        .domain([
                d3.max(words, function(d){return d.counter}),
                d3.min(words, function(d){return d.counter})
            ])
            .interpolate(d3.interpolateHcl)
            .range([d3.rgb(color_range[0]), color_range[1]]);


        words.forEach(function(d)  {
            d.size = font_value_scale(d.value)
        });


        var cloud = svg.selectAll("g text")
                        .data(words, function(d) { return d.text; })

        //Entering words
        cloud.enter()
            .append("text")
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .attr('font-family', "Impact")
            .text(function(d) { 
                return d.text; });

        //Entering and existing words
        cloud
            .style("font-size", function(d) { 
                return d.size + "px"; })
                .style("fill", function(d, i) { 
                    return color_counter_scale(d.counter); })
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .style("fill-opacity", 1);

        //Exiting words
        cloud.exit()
                .style('fill-opacity', 1e-6)
                .attr('font-size', 1)
                .remove();
    }


    //Use the module pattern to encapsulate the visualisation code. We'll
    // expose only the parts that need to be public.
    return {

        //Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        //The outside world will need to call this function, so make it part
        // of the wordCloud return value.

        update: function(words) {    
            var font_value_scale = d3.scale.linear()
            .domain([
                d3.min(words, function(d){return d.value}),
                d3.max(words, function(d){return d.value})])
            .range([20,50]);
    
            words.forEach(function(d)  {
                d.size = font_value_scale(d.value)
            });
            
            d3.layout.cloud().size([$(selector).width(), 500])
                .words(words)
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .fontSize(function(d) { 
                    return d.size; 
                })
                .on("end", draw)
                .start();

            
        }
    }

}

//Some sample data - http://en.wikiquote.org/wiki/Opening_lines


//Prepare one of the sample sentences by removing punctuation,
// creating an array of words and computing a random size attribute.
function getWords(i) {
    return words[i]
            .replace(/[!\.,:;\?]/g, '')
            .split(' ')
            .map(function(d) {
                return {text: d, size: 10 + Math.random() * 60};
            })
}

//This method tells the word cloud to redraw with a new set of words.
//In reality the new words would probably come from a server request,
// user input or some other source.
function showNewWords(vis, words) {
    vis.update(words)
    //setTimeout(function() { showNewWords(vis, i + 1)}, 2000)
}





