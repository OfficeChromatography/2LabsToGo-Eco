class flowRateGraph{
    constructor(numberOfDivisions){
        this.brd = JXG.JSXGraph.initBoard('box', {axis:true, boundingbox: [-20, 2.1, 120, -0.1]});
        this.lines={
            strokeOpacity:0.6,
            width:2,
            strokecolor:'black',
            fixed: true,
            elements:[]
        }
        this.gliders={
            elements: [],
            name: "a",
        };
        this.numberOfDivisions = numberOfDivisions
        this.graphPoints();
    }

    addLine(x){
        this.lines.elements.push(this.brd.create('segment',
            [[x, 0], [x, this.lines.width]],
            {
                fixed: this.lines.fixed,
                strokecolor: this.lines.strokecolor,
                strokeOpacity: this.lines.strokeOpacity
            }));
    }

    addGlider(lineIndex, y){
        this.gliders.elements.push(this.brd.create('glider',
            [0, y, this.lines.elements[lineIndex]],
            {name: this.gliders.name + lineIndex}));
    }

    graphPoints(){
        for (let i = 0; i <= this.numberOfDivisions; i++) {
            this.addLine(i * 100/this.numberOfDivisions)
            this.addGlider(i,1)
        }
        this.curve = this.brd.create('spline', this.gliders.elements, {strokecolor:'blue', strokeOpacity:0.6, strokeWidth:5});
    }

    saveSegment = function(toString){
        let data=[];
        for(let i = 0; i<this.gliders.elements.length;i++){
            let value = this.gliders.elements[i].Y().toFixed(2)
            data.push({"value": value})
        }
        if(toString){
            data = "&flowrate="+JSON.stringify(data)
        }
        return data;
    }
    
    loadSegment = function (flowrates) {
        this.brd.suspendUpdate();
        this.removeSegment();
    
        if (!Array.isArray(flowrates)) {
            this.numberOfDivisions = 5;
            this.graphPoints();
            this.brd.unsuspendUpdate();
            return;
        }
    
        flowrates.forEach(function (currentValue, index, array) {
            currentValue = parseFloat(currentValue.value);
            this.addLine(index * 100 / (array.length - 1));
            this.addGlider(index, currentValue);
        }, this);
    
        this.brd.removeObject(this.curve);
        this.curve = this.brd.create('spline', this.gliders.elements, {strokecolor:'blue', strokeOpacity:0.6, strokeWidth:5});
        this.brd.unsuspendUpdate();
    };

    removeSegment = function () {
        this.brd.suspendUpdate();
        this.gliders.elements.forEach(point => this.brd.removeObject(point))
        this.lines.elements.forEach(lines => this.brd.removeObject(lines))
        this.gliders.elements = []
        this.lines.elements = []
        this.brd.removeObject(this.curve);
        this.brd.unsuspendUpdate();
    };
}
var flowGraph

$("#flowrate_stepcontrol").on("change", function (){
    let steps=parseInt($(this).val())
    
    flowGraph = new flowRateGraph(steps)
})
