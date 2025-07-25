window.table = new Table(0, calcVol);

var getData = function(){
    data = $("form:not(.band-component)").serialize()+'&table='+JSON.stringify(table.getTableValues())
    return data
}

var setData = function (data){
  $.each(data,function (key,value,array){
    $('input[name='+key+']').val(value)
    if(key == "main_property"){
        $('select[name='+key+']').val(value)
    }
  })
  $(".change-graph-size-parameter").trigger("change")
  table.loadTable(data.bands_components)
  
}

var list_of_saved = new listOfSaved("http://127.0.0.1:8000/syringepump/save/",
    "http://127.0.0.1:8000/syringepump/list",
    "http://127.0.0.1:8000/syringepump/load",
    getData,
    setData,
    "http://127.0.0.1:8000/syringepump/delete",
    "syringe_pump"
    )

var application_control = new ApplicationControlSP('http://127.0.0.1:8000/oclab/control/',
                                                'http://127.0.0.1:8000/syringepump/start/',
                                                getData)

$(".change-graph-size-parameter").on("change", function(){
    changeGraphSize()
    mainCalculations()
    calcVol()
})

$(".change-bands-table").on("change", function(){
    //createBandsTable(getNumberBands())
    newComponentsTable(getNumberBands());
    calcVol()
})

$(".change-volume-parameter").on("change", function(){
    calcVol()
});

$("#id_main_property").on("change",function(){
        switch ($("#id_main_property").val()) {
            case '1':
                $("#id_valuesform").fadeOut();
                $("#id_valuesunit").html('#');
                $("#id_valuesform").fadeIn();
                $("#lengthbandsrow").hide();
                $("#nbandsrow").show();
                $("#valueLabel").text('Number')
                break;
            case '2':
                $("#id_valuesform").fadeOut();
                $("#id_valuesunit").html('[mm]');
                $("#id_valuesform").fadeIn();
                $("#bandlengthform").fadeIn();
                $("#nbandsrow").hide();
                $("#lengthbandsrow").show();
                $("#valueLabel").text('Length')
                break;
        }
        //createBandsTable()
        newComponentsTable(getNumberBands());
        $('.change-graph-size-parameter').trigger("change")
    });

function getNumberBands() {
  const gap_size = parseFloat($("#id_gap").val());
  const band_size = parseFloat($("#id_value").val());
  const property = $("#id_main_property").val();
  const working_area = nBandsWorkingArea();

  if (property === '1') {
      return parseFloat($("#id_value").val()); 
  } else if (property === '2') {
      return Math.trunc(working_area[0] / (band_size + gap_size));  
  }
  return 0;
}

function createBandsTable(number_bands = null){
    // gap_size = parseFloat($("#id_gap").val());
    // band_size = parseFloat($("#id_value").val());
    // property = $("#id_main_property").val();
    // number_bands = parseFloat($("#id_value").val());

    // working_area = nBandsWorkingArea()
    // if (property=='2'){number_bands = Math.trunc(working_area[0]/(band_size+gap_size))}
    newComponentsTable(number_bands);
}
// MAIN
function mainCalculations(){
    let plate_x_size = parseFloat($("#id_size_x").val());
    let plate_y_size = parseFloat($("#id_size_y").val());

    let offset_left_size = parseFloat($("#id_offset_left").val());
    let offset_right_size = parseFloat($("#id_offset_right").val());
    let offset_bottom_size = parseFloat($("#id_offset_bottom").val());

    let gap_size = parseFloat($("#id_gap").val());
    //let number_bands = parseFloat($("#id_value").val());
    const number_bands = getNumberBands();
    let band_size = parseFloat($("#id_value").val());

    let band_height = parseFloat($("#id_height").val());
    let property = $("#id_main_property").val();

  // Check if there are missing parameters
  missing_parameter = (isNaN(plate_x_size)||isNaN(plate_y_size)||isNaN(offset_left_size)||isNaN(offset_right_size)||isNaN(offset_bottom_size)||isNaN(gap_size)||isNaN(band_height))

  if(areErrors('#id_parameter_error',missing_parameter)){return}

  // Calculate the Working Area [x,y]
  working_area = nBandsWorkingArea()

  // Check if it's not posible to calculate the wa
  if(areErrors('#id_offsets_error',isNaN(working_area[0]) && isNaN(working_area[1]))){return}

  // Check if the vertical size is enough
  if(areErrors('#id_space_error',working_area[1]<band_height)){return}

  switch (property) {
    // N Bands
    case '1':
    //Gap process
      sum_gaps_size = totalGapLength(number_bands, gap_size)
      if(areErrors('#id_gap_error',isNaN(sum_gaps_size) || sum_gaps_size>= working_area[0])){return}

    //Bands Sizes
      band_size = totalBandsLength(working_area,sum_gaps_size,number_bands)
      if(areErrors('#id_space_error',isNaN(band_size))){return}
      break;
    // Length
    case '2':
      //number_bands = Math.trunc(working_area[0]/(band_size+gap_size))
      if(areErrors('#id_space_error',number_bands<1)){return}
      //createBandsTable(number_bands);
      newComponentsTable(number_bands);
      break;
  }

  plotPreview.eliminateAllPoints()
  for(i=0;i<number_bands;i++){
    newdata = []
    if(i==0){
      newdata[0]={y:offset_bottom_size,x:offset_left_size}
      newdata[1]={y:offset_bottom_size+band_height,x:offset_left_size}
      newdata[2]={y:offset_bottom_size+band_height,x:band_size+offset_left_size}
      newdata[3]={y:offset_bottom_size,x:band_size+offset_left_size}
      newdata[4]=newdata[0]
    }
    else{
      newdata[0]={y:offset_bottom_size,x:i*(band_size+gap_size)+offset_left_size}
      newdata[1]={y:offset_bottom_size+band_height,x:i*(band_size+gap_size)+offset_left_size}
      newdata[2]={y:offset_bottom_size+band_height,x:(i+1)*band_size+(gap_size*i)+offset_left_size}
      newdata[3]={y:offset_bottom_size,x:(i+1)*band_size+(gap_size*i)+offset_left_size}
      newdata[4]=newdata[0]
    }
    plotPreview.addData2Chart(i,'black', newdata)
  }
  plotPreview.update();
}

//  ERROR DISPLAY MANAGER
function areErrors(error_id, bolean_exp){
  if(bolean_exp){
    $(error_id).fadeIn();
    return true
  }
  else{
    $(error_id).fadeOut();
    return false
  }
}

//  Calculates the Working Area
function nBandsWorkingArea(){
    let plate_x_size = parseFloat($("#id_size_x").val());
    let plate_y_size = parseFloat($("#id_size_y").val());
    let offset_left_size = parseFloat($("#id_offset_left").val());
    let offset_right_size = parseFloat($("#id_offset_right").val());
    let offset_bottom_size = parseFloat($("#id_offset_bottom").val());

    working_area = [plate_x_size-offset_left_size-offset_right_size,plate_y_size-offset_bottom_size]
    if(working_area[0] <= 0 || working_area[1] <= 0 || isNaN(working_area[0]) || isNaN(working_area[1])){
        return [NaN,NaN];
    }
    else{
      return working_area;
    }
}

//  Calculate the sum of gaps lenght
function totalGapLength(number_bands, gap_size){
  number_of_gaps = number_bands - 1;
  if(number_of_gaps<0){
    return NaN
  }
  else{
    return gap_size*number_of_gaps;
  }
}

//  Calculate the sum of bands lenght
function totalBandsLength(working_area,sum_gaps_size,number_bands){
  bands_size = (working_area[0]-sum_gaps_size)/number_bands
  if(bands_size<=0){
    return NaN
  }
  else{
    return bands_size
  }
}



// Create a new Table with a given number of rows
// function newComponentsTable(number_row){
//     table.destructor()
//     table = new Table(number_row, calcVol);
// }

function newComponentsTable(desiredRows){
    const diff = desiredRows - table.numberOfRows;

    if (diff > 0){                  
        table.addEmptyRows(diff);
    } else if (diff < 0){           
        table.removeRowsFromEnd(-diff);
    }
    
}

// Change the Graph sizes with the size x and y field values.
function changeGraphSize(){
  plotPreview.config.options.scales.xAxes[0].ticks.max = parseFloat($("#id_size_x").val());
  plotPreview.config.options.scales.yAxes[0].ticks.max = parseFloat($("#id_size_y").val());
  plotPreview.update();
}



var calcVol = function calcVol(){

  $formData = $('#plateform').serialize()+'&'+$('#movementform').serialize()+'&table='+JSON.stringify(table.getTableValues())
  $endpoint = window.location.origin+'/syringepumpcalc/'
  $.ajax({
  method: 'POST',
  url:    $endpoint,
  data:   $formData,
  success: calcMethodSuccess,
  error: calcMethodError,
  })

  function calcMethodSuccess(data, textStatus, jqXHR){
    table.setTableCalculationValues(data.results.slice(0,-1))
    table.estim_time(data.results.slice(-1))
  }
  function calcMethodError(jqXHR, textStatus, errorThrown){
    console.error("Error calculating estimated volumes", errorThrown)
    }
}


$(document).ready(function() {
  //createBandsTable()
  const defaultValue = parseFloat($("#id_value").val());
  createBandsTable(defaultValue);
  calcVol()
  list_of_saved.loadList()
});

