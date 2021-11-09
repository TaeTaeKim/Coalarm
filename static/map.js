google.charts.load('current', {'packages':['geochart']});
google.charts.setOnLoadCallback(drawRegionsMap);

  function drawRegionsMap() {
    // const data = google.visualization.arrayToDataTable([
    //   ['Country', 'Popularity','Exp'],
    //   ['Germany', 200,1000],
    //   ['United States', 300,100000],
    //   ['Brazil', 400,50000],
    //   ['Canada', 500,0],
    //   ['France', 600,0],
    //   ['RU', 700,0],
    //   ["KR",1000,100]
    // ]);
    const data = new google.visualization.DataTable();
      data.addColumn('string','Country');
      data.addColumn('number','active_case')
    //   for(let i=0;i<data.length;i++){
    //       data.addRows([
    //           [{v:`${}`,f:`${}`},`${}`]
    //       ])
    //   }
      data.addRows([
          [{v:'KR',f:'South Korea'},100000]
      ])
    const options = {
        legend:'none',
        colorAxis: {colors: ['#00853f', 'black', '#e31b23']},
        backgroundColor: '#81d4fa',
        defaultColor: '#f5f5f5'
    };

    const chart = new google.visualization.GeoChart(document.getElementById('regions_div'));
    google.visualization.events.addListener(chart,'select', function(){
        let selection = chart.getSelection();
        console.log(selection);
        if (selection.length == 1) {
            var selectedRow = selection[0].row;
            var selectedRegion = data.getValue(selectedRow, 0);
            // window.location.href = 'https://www.naver.com/';
            console.log(selectedRegion);
        }
    });
    chart.draw(data, options);
  }