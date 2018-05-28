function generate_datatable(selector, data_url){ 
    $.fn.dataTable.render.moment( 'DD/MM/YYYY HH:MM');
    

    table =  $(selector).DataTable( {
        "ajax": data_url,
        "mark": true,
        "language": {
        "url": "assets/i18n/Italian.json"
        },
        "createdRow": function( row, data, dataIndex){
        if( data.username ==  "luigidimaio"){
            $(row).addClass('redClass');
        }
        else{
            $(row).addClass('greenClass');
        }
    },              
        "columns": [{ 
            "title": "Data", 
            "width": "15%", 
            "data": function(d){ 
                return new Date(d.original_date)},
            "render":$.fn.dataTable.render.moment( 'DD/MM/YYYY HH:MM'), 
        }, {
            "title": "Autore",
            "data": "by"
        }, { 
            "data": "text" , 
            "title": "Testo"},
        {
            "className":      'details-control',
            "orderable":      false,
            "data":           null,
            "defaultContent": '<span class="glyphicon glyphicon-info-sign" aria-hidden="true"></span>'
        },
    
    ],
    "order": [[0, 'desc']]
    } );
    
    

    function format ( d ) {

        console.log(d)
        // `d` is the original data object for the row
        return '<div class="table-content">'+
        '<blockquote class="embedly-card" data-card-controls="0"><h4><a href="' +
        d.post_link +'"></a></h4><p>' +
        d.text + '</p></blockquote>'+
        '</div><script async src="//cdn.embedly.com/widgets/platform.js" charset="UTF-8"></script>';
    }



    $("#message-table").on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );
    
    
    return table
}


function generate_control_slider(selector, slide_max, start, handler){ 

    var slider = document.getElementById(selector);
    noUiSlider.create(slider, {
        start: [ start ], // Handle start position
        step: 1, // Slider moves in increments of '10'
        margin: 20, // Handles must be more than '20' apart
        range: { // Slider can select '0' to '100'
            'min': 0,
            'max': slide_max
        },

    });  
    slider.noUiSlider.on('change', handler);
    return slider
}


  
  function count_words(x){
    return (x.length) ? d3.sum(x, function(d){return d.counter}) : 0;
  };
  
  function filter_words(x, word){
    return x.filter(function(d){ return x.text == word });
  };


  function format_data(data, username){
      var iso = d3.time.format.utc("%Y-%m-%dT%H:%M:%S.%LZ");
      
      data.forEach(function(d) { 
          d["date"] = iso.parse(d["created_at"]);
          d["count_total"] = count_words(d.score);
          d["username"] = username;
      });
      return data;
  };


  function extract_ordered_datelist(data){
      var min_date = d3.min(data, function(d){return d.date});
      var max_date = d3.max(data, function(d){return d.date});
      var date_list = []
      for (i = 0; i < data.length; i++) {
          date_list.push(data[i].date); 
      }
      return [min_date, max_date, date_list]
  }

  function select_words_by_date(data, value){ 
    var selected = data.filter(function(d){ 
        return (d.date.getTime() == value.getTime()) ?  d : null})
    return selected[0]["score"]
  }
      
  function update_word_cloud(words, world_cloud, number=30, value="value"){
    words.sort(function(a, b){ return d3.descending(a[value], b[value]) })
    words = words.slice(0, number)
    showNewWords(world_cloud, words, value);
    return world_cloud
  }


  function read_dataset(path){
    var dataset; 
    d3.json(path, function(data){ 
            dataset = data
        })
    
    return dataset
  } 

  function reset_words_chart(text){
    text.classed("select", false)
    text.style("opacity", "1")
  }
  function clone_array(array){
    return array.map(a => Object.assign({}, a));
  }

  function get_ita_month_year(date){
    var monthNames = [ "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
      "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre" ];
      return monthNames[date.getUTCMonth()]+' '+date.getUTCFullYear();
  }
