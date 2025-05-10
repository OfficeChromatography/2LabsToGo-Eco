document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('import_csv_file').addEventListener('change', function(event) {
        var reader = new FileReader();
        reader.onload = function(e) {
            processCSV(e.target.result);
        };
        reader.readAsText(event.target.files[0]);
    });
});

function processCSV(csvData) {
    var lines = csvData.trim().split("\n");
    var result = {};
    var colorSelected = [];
    var defaultImageUrl = 'http://127.0.0.1:8000/static/img/login.jpg';
    lines.forEach(function(line) {
        
        let firstCommaIndex = line.indexOf(',');
        let key = line.substring(0, firstCommaIndex).trim();
        let value = line.substring(firstCommaIndex + 1).trim();
        value = decodeURIComponent(value);
        result[key] = value;
    });
    result['image_id'] = defaultImageUrl;
    
    result['selected-element-id'] = "";
    loadDataIntoForm(result, colorSelected);
}

function loadDataIntoForm(data, colorSelected) {
    Object.keys(data).forEach(function(key) {
        
        if (["red", "green", "blue"].includes(key)) {
            return; 
        }
        if (key === "image_id") {
            var image = document.getElementById('image_id');
            if (image) {
                image.src = data[key];
                image.alt = data[key];
            } 
        } else if (key === "note") {
            var noteTextArea = document.getElementById('notestextarea');
            if (noteTextArea) {
                noteTextArea.value = data[key];
            }
        } else {
            var safeKey = (typeof CSS !== 'undefined' && CSS.escape) 
                ? CSS.escape(key) 
                : key.replace(/(["\\])/g, '\\$1');
            var input = document.querySelector(`[name="${safeKey}"]`);
            if (input) {
                input.value = data[key];
                input.dispatchEvent(new Event('change', { bubbles: true }));
            } else {
                console.warn("No input found for key:", key);
            }
        }
    });
    
    let redValue   = data.red || "0";
    let greenValue = data.green || "0";
    let blueValue  = data.blue || "0";
    
    let redInput   = document.querySelector('[name="color_red"]');
    let greenInput = document.querySelector('[name="color_green"]');
    let blueInput  = document.querySelector('[name="color_blue"]');
    
    if (redInput) {
        redInput.value = redValue;
        redInput.dispatchEvent(new Event('change', { bubbles: true }));
    }
    if (greenInput) {
        greenInput.value = greenValue;
        greenInput.dispatchEvent(new Event('change', { bubbles: true }));
    }
    if (blueInput) {
        blueInput.value = blueValue;
        blueInput.dispatchEvent(new Event('change', { bubbles: true }));
    }

    $('#picker').colpickSetColor({
        r: redValue,
        g: greenValue,
        b: blueValue
    });
    $('#import_csv_file').val('');
  
}

$('#exportbttn').on('click', function (ev) {
    ev.preventDefault()
    var element = document.createElement('a');
    element.setAttribute('href', $('#image_id').attr('src'));
    element.setAttribute('download', $('#image_id').attr('name'));
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
})

$('#image_new_tab_bttn').on('click', function (ev) {
    ev.preventDefault()
    window.open($('#image_id').attr('src'))
})

$('#delete_image').on('click', function (ev) {
    ev.preventDefault()
    id = $("#image_id").attr('alt')
    $.ajax({
      type: 'DELETE',
      url:    window.location.origin+'/capture/delete/'+ id,
      success: deleteMethodSuccess,
      error: deleteMethodError,
    });
})
function deleteMethodSuccess(id, textStatus, jqXHR){
    list_of_saved.loadList()

}
function deleteMethodError(jqXHR, textStatus, errorThrown){console.log('error')}







