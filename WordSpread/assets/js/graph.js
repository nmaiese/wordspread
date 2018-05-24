function generate_control_slider(selector, slide_max, handler){ 
    $(selector).slider({
      min: 0,
      max: slide_max,
      step: 1,
      value: 0,
      slide: handler
      })
    //$( "#slider" ).val((date_list[$(selector).slider("value")]).toDateString());
  }
      
  function formate_data(data){
      var iso = d3.time.format.utc("%Y-%m-%dT%H:%M:%S.%LZ");
      data.forEach(function(d) { 
          d["date"] = iso.parse(d["created_at"]) 
      });
      return data
  }

  function extract_ordered_datelist(data){
      var min_date = d3.min(data, function(d){return d.date})
      var max_date = d3.max(data, function(d){return d.date})
      console.log()
      var date_list = []
      for (i = 0; i < data.length; i++) {
          date_list.push(data[i].date); 
      }
      return [min_date, max_date, date_list]
  }

  function select_words_by_date(data, value){ 
    var selected = data.filter(function(d){ return (d.date = value) ?  d : null})
    return selected[0]["score"]
  }
      
  function update_word_cloud(words, world_cloud){
    console.log(words)
    words.sort(function(a, b){ return d3.descending(a.value, b.value) })
    words = words.slice(0, 20)
    showNewWords(world_cloud, words);
    return world_cloud
  }


  function read_dataset(path){
    var dataset; 
    d3.json(path, function(data){ 
            dataset = data
            console.log(dataset)
        })
    
    return dataset
  } 