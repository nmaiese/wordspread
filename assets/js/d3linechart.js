/**
 * User: nross
 */


var monthNames = [ "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre" ];

var maxDataPointsForDots = 50,
	transitionDuration = 500;

var svg = null,
	yAxisGroup = null,
	xAxisGroup = null,
	dataCirclesGroup = null,
	dataLinesGroup = null;

// var tooltip = floatingTooltip('photo-tooltip', 240);

function lineChart(data, data_two, selector, highilight=null) {
	var w = $(selector).width();
    h = 250;

    function sortByDateAscending(a, b) {
        // Dates will be cast to numbers automagically:
        return b.date - a.date ;
    }

    function showDetail(d) {
    //   change outline to indicate hover state.
    //   d3.select(this).attr('stroke', 'black');
    //   var content =  '<div class="row linechart-ttip">' +
    //     '<div class="col-md-12 ttip-time"><b>Day</b>: ' + printTime(d.date) + '</div><br/>' +
    //     '<div class="col-md-12 ttip-interactions"><b>'+ interaction_selected + '</b>: ' + d.count_total + '</div></div>'
    //   tooltip.showTooltip(content, d3.event);
    }

    function hideDetail(d) {
    //     // reset outline
    //     d3.select(this)
    //     //.attr('stroke', d3.rgb(colors.range()[d.cluster]).darker());
    //     tooltip.hideTooltip();
    }
	
	data = data.sort(sortByDateAscending);
	data_two = data_two.sort(sortByDateAscending);

	var margin_left = (w>500) ? 50 : 40 ;
	var margin_top = 20;
	var margin_bottom = 40;
	var margin_right = 10; 
	var max = d3.max(data, function(d) { return d.count_total });
	max = (max>=d3.max(data_two, function(d) { return d.count_total })) ? max : d3.max(data_two, function(d) { return d.count_total })
	var min = 0;
	var max_date = d3.max(data, function(d) { return d.date });
	var min_date = d3.min(data, function(d) { return d.date });

	var pointRadius = 4;

	var x = d3.time.scale().range([0, w - margin_left * 2]).domain([min_date, max_date]);
	var y = d3.scale.linear().range([h - margin_bottom * 2, 0]).domain([min, max]);

	var xAxis = d3.svg.axis().scale(x).tickSize(h - margin_bottom * 2).tickPadding(10).ticks(7);
	var yAxis = d3.svg.axis().scale(y).orient('left').tickSize(-w + margin_left * 2).tickPadding(15).ticks(3).tickFormat(d3.format(".0f"));
	var t = null;

	svg = d3.select(selector).select('svg').select('g');

	if (svg.empty()) {
		svg = d3.select(selector)
			.append('svg:svg')
				.attr('width', w)
				.attr('height', h)
				.attr('class', 'viz')
			.append('svg:g')
				.attr('transform', 'translate(' + margin_left + ',' + margin_top + ')');
	}

    var defs = svg.append("defs");
    var gradient = defs.append("linearGradient")
        .attr("id", "svgGradient")
        .attr("x1", "0%")
        .attr("x2", "0%")
        .attr("y1", "100%")
        .attr("y2", "0%");

    gradient.append("stop")
        .attr('class', 'start')
        .attr("offset", "0%")
        .attr("stop-color", "#fff")
        .attr("stop-opacity", 1);

    gradient.append("stop")
        .attr('class', 'end')
        .attr("offset", "100%")
        .attr("stop-color", "#79e779")
        .attr("stop-opacity", 1);

	t = svg.transition().duration(transitionDuration);

	// y ticks and labels
	if (!yAxisGroup) {
		yAxisGroup = svg.append('svg:g')
			.attr('class', 'yTick')
			.call(yAxis);
	}
	else {
		t.select('.yTick').call(yAxis);
	}

	// x ticks and labels
	if (!xAxisGroup) {
		xAxisGroup = svg.append('svg:g')
			.attr('class', 'xTick')
			.call(xAxis);
	}
	else {
		t.select('.xTick').call(xAxis);
	}

	// Draw the lines
	if (!dataLinesGroup) {
		dataLinesGroup = svg.append('svg:g');
	}

	var dataLines = dataLinesGroup.selectAll('.data-line')
			.data([data]);
	
	var dataLines_two = dataLinesGroup.selectAll('.data-line2')
		.data([data_two]);

	var line = d3.svg.line()
		.x(function(d,i) { return x(d.date); })
		.y(function(d) { return y(d.count_total); })

	line.interpolate("monotone")
	var garea = d3.svg.area()
		.x0(x(highilight)-40)
		.x1(x(highilight)+40)
        .y0(h - margin_bottom * 2)
		.y1(function(d) { return y(y.domain()[1]); });

    garea.interpolate("monotone")

	dataLines.enter().append('path')
		 .attr('class', 'data-line')
		 .style('opacity', 0.3)
		 .attr("d", line(data));
	

	dataLines_two.enter().append('path')
		 .attr('class', 'data-line2')
		 .style('opacity', 0.3)
		 .attr("d", line(data_two));

		 
	dataLines.enter().append('svg:rect')
		.attr("class", "area")
		.style("fill", "#dcdcdc")
		.style("opacity", 0.5)
		.attr("x", x(highilight)-((x(highilight)-20)>0) ?  x(highilight)-20 : 0)
		.attr("width", ((x(x.domain()[1])-x(highilight))>0) ?  40 : 0)
		.attr("y", function(d) { return y(y.domain()[1]); })
		.attr("height", h - margin_bottom * 2);
		


	dataLines
		.attr("d", line)
			.style('opacity', 1)


	d3.selectAll(".area").transition()
	.style("fill", "#dcdcdc")
	.style("opacity", 0.5)
	.attr("x", x(highilight)-((x(highilight)-20)>0) ?  x(highilight)-20 : 0)
	.attr("width", ((x(x.domain()[1])-x(highilight))>0) ?  40 : 20)
	.attr("y", function(d) { return y(y.domain()[1]); })
	.attr("height", h - margin_bottom * 2);
	

	dataLines_two.transition()
		.attr("d", line)
		.duration(transitionDuration)
			.style('opacity', 1)
				
	dataLines.exit()
		.transition()
		.attr("d", line)
		.duration(transitionDuration)
                        .attr("transform", function(d) { return "translate(" + x(d.date) + "," + y(0) + ")"; })
			.style('opacity', 1e-6)
			.remove();

	dataLines.exit()
		.transition()
		.attr("d", garea)
		.duration(transitionDuration)
						.attr("transform", function(d) { return "translate(" + x(d.date) + "," + y(0) + ")"; })
			.style('opacity', 1e-6)
			.remove();
	

	dataLines_two.exit()
	.transition()
	.attr("d", line)
	.duration(transitionDuration)
					.attr("transform", function(d) { return "translate(" + x(d.date) + "," + y(0) + ")"; })
		.style('opacity', 1e-6)
		.remove();
					
	// Draw the points
	if (!dataCirclesGroup) {
		dataCirclesGroup = svg.append('svg:g');
	}

	var circles = dataCirclesGroup.selectAll('.data-point')
		.data(data);
	var circles_two = dataCirclesGroup.selectAll('.data-point2')
		.data(data_two);

	circles
		.enter()
			.append('svg:circle')
				.attr('class', 'data-point')
				.style('opacity', 1e-6)
				.attr('cx', function(d) { return x(d.date) })
				.attr('cy', function() { return y(0) })
				.attr('r', function() { return 10 })
				.on('mouseover', showDetail)
                .on('mousemove', showDetail)
                .on('mouseout', hideDetail)
			.transition()
			.duration(transitionDuration)
				.style('opacity', 0)
				.attr('cx', function(d) { return x(d.date) })
				.attr('cy', function(d) { return y(d.count_total) });

	circles_two
		.enter()
			.append('svg:circle')
				.attr('class', 'data-point2')
				.style('opacity', 1e-6)
				.attr('cx', function(d) { return x(d.date) })
				.attr('cy', function() { return y(0) })
				.attr('r', function() { return 10 })
				.on('mouseover', showDetail)
                .on('mousemove', showDetail)
                .on('mouseout', hideDetail)
			.transition()
			.duration(transitionDuration)
				.style('opacity', 0)
				.attr('cx', function(d) { return x(d.date) })
				.attr('cy', function(d) { return y(d.count_total) });

	circles
		.transition()
		.duration(transitionDuration)
			.attr('cx', function(d) { return x(d.date) })
			.attr('cy', function(d) { return y(d.count_total) })
			.attr('r', function() { return (data.length <= maxDataPointsForDots) ? pointRadius : 0 })
			.attr('r', function() { return 10 })
			.style('opacity', 0);


	circles_two
		.transition()
		.duration(transitionDuration)
			.attr('cx', function(d) { return x(d.date) })
			.attr('cy', function(d) { return y(d.count_total) })
			.attr('r', function() { return (data.length <= maxDataPointsForDots) ? pointRadius : 0 })
			.attr('r', function() { return 10 })
			.style('opacity', 0);


	circles
		.exit()
			.transition()
			.duration(transitionDuration)
				// Leave the cx transition off. Allowing the points to fall where they lie is best.
				//.attr('cx', function(d, i) { return xScale(i) })
				.attr('cy', function() { return y(0) })
				.style("opacity", 1e-6)
				.remove();
	circles_two
		.exit()
			.transition()
			.duration(transitionDuration)
				// Leave the cx transition off. Allowing the points to fall where they lie is best.
				//.attr('cx', function(d, i) { return xScale(i) })
				.attr('cy', function() { return y(0) })
				.style("opacity", 1e-6)
				.remove();
}




