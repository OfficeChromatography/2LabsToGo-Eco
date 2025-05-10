class ApplicationControlDev {
    constructor(control_url, play_url, getData) {
      this.state = "stopped"; // "started" o "stopped"
      this.control_url = control_url;
      this.play_url = play_url;
      this.getData = getData;
  
      this.$startButton = $("#start_bttn_dev");
      this.$stopButton = $("#stop_bttn_dev");
  
      this._handleStartClick();
      this._handleStopClick();
    }
  
    _changeState() {
      switch (this.state) {
        case "started":
          $(".application-control").find(".btn")
            .removeClass()
            .addClass("btn btn-success");
          break;
        case "stopped":
          $(".application-control").find(".btn")
            .removeClass()
            .addClass("btn btn-info");
          break;
      }
    }
  
    _handleStartClick() {
      this.$startButton.on("click", () => {
        this._start();
      });
    }
  
    _handleStopClick() {
      this.$stopButton.on("click", () => {
        this._stop();
        sendToMachine('M92Z400')
        sendToMachine('M203Z40')   
        sendToMachine('M42P49S0')
        sendToMachine('M42P36S0')
        sendToMachine('G28YX');
      });
    }
  
    _start() {
    
     $.post(this.play_url, this.getData())
        .done(() => {
          this.state = "started";
          this._changeState();
          this.$startButton.text("Start");
        });
    }
    
    _stop() {
      $.post(this.control_url, { STOP: '' })
        .done(() => {
          this.state = "stopped";
          this.$startButton.text("Start");
          this._changeState();
        });
    }
  }
 
