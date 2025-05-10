class ApplicationControlAS{
    constructor(control_url, play_url,getData){
        this.state = "stopped" // started, stopped
        this.control_url = control_url
        this.play_url = play_url
        this.getData = getData
        this.$click_start_button_handler()
        this.$click_stop_button_handler()
    }
    $change_state(){
        switch (this.state){
            case "started":
                $(".application-control").find(".btn").removeClass().addClass("btn btn-success")
            break;
            case "stopped":
                $(".application-control").find(".btn").removeClass().addClass("btn btn-info")
            break;
            
        }
    }

    $click_start_button_handler(){
        
        let application_control = this
        $("#start_bttn_as").on("click",function(){
            console.log("START")
            application_control.$start();
        })
    }

    $click_stop_button_handler(){
        let application_control = this
        $("#stop_bttn_as").on("click",function(){
            application_control.$stop()
            sendToMachine('M42P40S0')
            sendToMachine('G90')
            sendToMachine('G0E0')
            sendToMachine('M400')
            sendToMachine('G28Z')
            sendToMachine('G28YX')
            sendToMachine('M155S0')
            sendToMachine('M140S0');
        })
    }


    $start(){
        $.post(application_control.play_url,application_control.getData()).done(function(){
                    console.log("STOP")
                    application_control.state = "started"
                    application_control.$change_state()
                    $(this).text("Start")
                    }
        )
    }

    $stop(){
        $.post(application_control.control_url,{STOP:''}).done(function(){
                application_control.state = "stopped"
                $("#start_bttn").text("Start")
                application_control.$change_state()
                }
        )
    }
    

}
