$(document).ready(function() {
  
  const lengthMappings = {
    3: 40,
    6: 50,
    12: 60,
  };
  
  const syringeLengthField = $("#id_length_type");
  
  function updateLengthField(selectedVolume) {
    if (lengthMappings[selectedVolume]) {
      syringeLengthField.val(lengthMappings[selectedVolume] + " mm");
      
    } else {
      syringeLengthField.val('');
    }
  }

  const defaultSelectedVolume = parseFloat($("#id_volume_type").val());
  updateLengthField(defaultSelectedVolume);
  let selectedVolume = 3;
  $("#id_volume_type").on("change", function() {
    selectedVolume = parseFloat($(this).val());
    updateLengthField(selectedVolume);
  });

  
  $("#changeSyringeType").on("click", function(e) {
    e.preventDefault();

    const actualVolumeMappings = {
      "2": 3,
      "5": 6,
      "10": 12,
    };

    
    const submittedData = {
      'volume_type': selectedVolume,
      'length_type': lengthMappings[selectedVolume]
    };

  
    $.ajax({
      method: 'POST',
      url: window.location.origin + '/syringetype/',
      data: submittedData,
      success: function(data) {
    
      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log("error", data);
      
      },
    });
  });

});
