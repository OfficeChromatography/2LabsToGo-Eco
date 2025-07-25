class listOfSaved{
    constructor(save_url, list_url, get_url, saveEvent, loadEvent, delete_app_url,list_option){
        this.save_url = save_url;
        this.list_url = list_url;
        this.get_url = get_url;
        this.saveEvent = saveEvent;
        this.loadEvent = loadEvent;
        this.delete_app_url = delete_app_url;
        this.delete_method_url = 'http://127.0.0.1:8000/method/delete/';

        this.$click_new_button_handler()
        this.$click_save_button_handler()
        this.$click_export_button_handler()
        this.type_list = list_option;
        this.saveIDs=[];
    }
    $renderListInScreen = (elements) => {
        // Render list of saved in screen
        
        if(this.type_list === "autosampler")
        {
            this.$cleanList()
            elements.forEach(element =>{ 
                if((element[2][0]===1) && (element[2][1]===0.3) && (element[2][3]===1)){
                    this.$addToList(element)
                 }
               
            })
        }
        else if (this.type_list === "development")
        {
            
            this.$cleanList()
            elements.forEach(element =>{ 
                if((element[2][0]===0.3) && (element[2][1]===1)){
                    this.$addToList(element)
                 }
            })
        }
        else if (this.type_list === "detection")
            {
                this.$cleanList()
                elements.forEach(element =>{ 
                    if((element[2][0]===0.3) && (element[2][1]===0.3)){
                        this.$addToList(element)
                     }
                })
            }
        else if (this.type_list === "syringe_pump")
            {
                this.$cleanList()
                elements.forEach(element =>{ 
                    if((element[2][0]===1) && (element[2][1]===0.3) && (element[2][3]===0)){
                        this.$addToList(element)
                        }
                })
            }
        else {
            this.$cleanList()
            elements.forEach(element => this.$addToList(element))
                   
            }
        

    }
    

    $afterListRendered = () =>{
        // After rendering, load the first or create a new method
        if($("#list-load").children().length>0){
            this.$loadEventsHandler();
            $("#list-load a").first().trigger("click")
        }
        else{
            $("#new_method_bttn").trigger("click")
        }
    }


    loadList(){
        // Query the elements
        $.get( this.list_url, (data) => this.$renderListInScreen(data))
            .done(()=>this.$afterListRendered())
    }

    $cleanList(){
        $('#list-load').empty()
    }

    $addToList(element){
        //Add the new item to the List
        let newListObject = this.$newListElement(element[0],element[1],element[2])
        $('#list-load').append(newListObject)
    }

    $newListElement(text, db_id, iconOpacity){
        // Creates the new element in list
        let flex_container = $("<div class=\"d-flex py-0 flex-row justify-content-between align-items-center\"></div>")
        let element = $("<a class=\"saved_element py-2\" style=\"width:100%\">"+ text +"</a>")
        let trash_can = $("<i class=\"fas fa-trash saved_element_trash_can\"></i>")

        flex_container.addClass('list-group-item list-group-item-action')
        flex_container.attr('role','tab')
        flex_container.attr('href','#list-home')
        flex_container.attr('data-toggle','list')
        flex_container.attr('aria-controls',"home")

        element.attr('value_saved',db_id)

        flex_container.append(element,trash_can) 
        return flex_container
    }

    $loadEventsHandler(){
        this.$click_element_handler()
        this.$delete_element_handler()
    }

    $click_element_handler(){
        $(".saved_element").on("click", (e) => this.$get_element_data($(e.currentTarget)))
    }

    $delete_element_handler(){
        $(".saved_element_trash_can").on("dblclick click mouseover mouseout", (e) => {
            switch (e.type){
                case "dblclick":
                    
                    this.$delete_method_element($(e.currentTarget).siblings('a'))
                    this.$delete_method_element($(e.currentTarget).hide())
                    break;
                case "click":
                    this.$delete_element_completely($(e.currentTarget).siblings('a'))
                    this.$delete_element_completely($(e.currentTarget).hide())
                    break;
                case "mouseover":
                    $(e.currentTarget).animate({
                        opacity: '0.3'
                    });
                    break;
                case "mouseout":
                    $(e.currentTarget).animate({
                        opacity: '1'
                    });
                    break;
            }
        })
    }

    $click_new_button_handler(){
        
        $("#new_method_bttn").on("click",function(){
            if ($('#notestextarea').length) {
                $('#notestextarea').val(''); 
                $('#image_id').attr('src', $('#image_id').data('default-src'));
                $('#image_id').attr('alt', 'Imagen por defecto');
            }
            
        if ($('#waitingTimeTableBody').length) {
            
            if (table_obj) {
                table_obj.waitingTimesData = []; 
                table_obj.generateEmptyRows();  
            }
        }
            $('#new_filename').prop('readonly', false);
            $("#list-load").find("a.active").removeClass("active")
            $('#new_filename').val("")
            $('#selected-element-id').val("")
             if (window.table){
                table.destructor();
                const filas = parseInt($("#id_value").val()) || 0;
                window.newComponentsTable(filas);
             }
        }
    )
    }

    $click_save_button_handler(){
        $("#save_bttn").on("click", (e) => {
            e.preventDefault()
            let data = this.saveEvent()
            this.$save(data)
            $('#new_filename').prop('readonly', true);
        })
    }

    $save(data){
        $.post( this.save_url, data)
        .done(()=>{
            this.loadList()})
        .fail()
        .always();
    }

    $delete_method_element(object) {
        const valueSaved = object.attr("value_saved");
        if (valueSaved !== undefined) {
            $.ajax({
                url: this.delete_method_url + "/" + valueSaved,
                type: 'DELETE',
            })
            .done(() => {
                object.parent().remove(); // Remove the list item from the DOM
                this.loadList();
            })
            .fail()
            .always();
        }
        
    }
    
    $delete_element_completely(object) {
        const valueSaved = object.attr("value_saved");
        if (valueSaved !== undefined) {
            $.ajax({
                url: this.delete_app_url + "/" + valueSaved,
                type: 'DELETE',
            })
            .done(() => {
                object.parent().remove(); 
                this.loadList();
            })
            .fail()
            .always();
        }
    }


    $get_element_data(e){
        //Gets the data save it in data_received
        $.get(this.get_url+"/"+e.attr('value_saved')+"/").done((data)=>{
            this.data_received = data
            $('#new_filename').val(data.filename)
            $('#selected-element-id').val(data.id)
            this.loadEvent(data)
        })
    }

    $click_export_button_handler(){
        $("#export_bttn").on("click",(e) => {
            e.preventDefault();
            this.$exportToCsv();
        })
    }
    $exportToCsv = function () {
        let data = this.saveEvent();
        let sentencias = data.replaceAll('&', '\n');
        sentencias = sentencias.replaceAll('=', ',');
        
        if (window.location.pathname.includes('development')) {
            const urlParams = new URLSearchParams(data);
            const waitingTimesEncoded = urlParams.get('waitingTimes');  
            let waitingTimes = [];
            if (waitingTimesEncoded) {
                try {
                    waitingTimes = JSON.parse(decodeURIComponent(waitingTimesEncoded));
                } catch (error) {
                    console.error("Error al decodificar waitingTimes:", error);
                }
        }
    sentencias = sentencias.replaceAll('=', ',');
    sentencias = sentencias.split('\n').filter(line => !line.startsWith('waitingTimes,')).join('\n');

    if (waitingTimes.length > 0) {
        sentencias += '\n\nWaiting Time Data';

        waitingTimes.forEach((wt, index) => {
            sentencias += `\napplication_${wt.application},${wt.waitTime}`;
        });
    } else {
        console.error("No se encontraron datos de waitingTimes");
    }
    
        }
    
        var hiddenElement = document.createElement('a');
        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(sentencias);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'output.csv';
        hiddenElement.click();
    };
    
    
}







