//humidity control 2LabsToGo-Eco

$fn=80;
h=38; //box height
hf=28; //fan height

box();
//lid();
//drawer();
//drawer_handle();
//front_extension();

module box() {
difference() {
    union() {
        cube([60, 190, 3]);
        translate([10, 20+7, 3]) cube([47, 4, h]);
        translate([10, 20+7, 3]) cube([4, 155-7, h]);
        translate([60-4, 20+7, 3]) cube([4, 155-7, h]);
        translate([10, 145+30, 3]) cube([50, 4, h]);
        
        //z1 motor cover
        translate([32.5-21-2, 0, 3]) cube([2, 28, 10]);
       translate([32.5+21, 0, 3]) cube([2, 28, 10]); 
        translate([32.5-21-2, 26, 3]) cube([44, 2, 10]);
    }
    //cutouts
    //cutout z1 spindle
       translate([32.5, 5.1, -1]) cylinder(d=8.2, h=5);
       translate([32.5-8.2/2, -1, -1]) cube([8.2, 6.1, 5]);
    //cutout suction opening
    translate([10+4, 134, -1]) cube([42, 30, 6]);
    //cutout fan
    translate([35, 30+21, -1]) cylinder(d=38, h=5);
    //holes fan screws
    translate([10+3+4+2, 30+21-16, -1]) cylinder(d=3.3, h=6);
    translate([10+3+4+32+2, 30+21-16, -1]) cylinder(d=3.3, h=6);
    translate([10+3+4+2, 30+21+16, -1]) cylinder(d=3.3, h=6);
    translate([10+3+4+32+2, 30+21+16, -1]) cylinder(d=3.3, h=6);
    //cutout drawer
    rotate([90, 0, 90]) translate([30+20+23, 3, 55])  cutout_drawer(); 
    //holes for screws
    for (i=[0:2])
    translate([6, 6+i*89, -1]) cylinder(d=3.2, h=5);
    translate([60-2, 6, -1]) cylinder(d=3.2, h=5);
    translate([60-6, 190-6, -1]) cylinder(d=3.2, h=5);
    }
}

module lid() {
    cube([50, 155+3-6, 3]);
}

module drawer() {
    difference() {
        linear_extrude(height = 46, scale = 1) 
    polygon(points=[[0,0],[0,hf-0.3],[60-0.3,h-0.2], [60-0.3,0]]);
        translate([2, 2, 2])
        linear_extrude(height = 46-4, scale = 1)  polygon(points=[[0,0],[0,hf-6],[60,h-6], [60,0]]);
   
    a=(h-hf)/60; //arctan
    b=a*180/3.14;  //rad in °
    //1.5 mm slits
    for(x=[3:3:42])
    translate([2, hf-5, x]) rotate([0, 0, b]) cube([20, 6, 1.5]);
    //1 mm slits
    //for(x=[3:2:44])
    //translate([2, hf-5, x]) rotate([0, 0, b]) cube([20, 6, 1]); 
    }
    translate([60-2.2, h-2.2, 0]) cube([2, 2, 46 ]);
}

module cutout_drawer() {
    linear_extrude(height = 10, scale = 1) 
    polygon(points=[[0,0],[0,h],[60,h], [60,0]]);
}

module drawer_handle() {
    translate([95-3-3+3, -3, 0]) cube([3, 66, h+3]);
    translate([95-3-3+3, -3, 13]) cube([10, 66, 3]);
    translate([95-3+10, -3, 14]) rotate([-90, 0, 0]) cylinder(d=6, h=66);
}

module fan( ) {
    difference() {
    hull() {
        translate([3, 3, 0]) cylinder(d=6, h=28);
        translate([40-3, 3, 0]) cylinder(d=6, h=28);
        translate([3, 40-3, 0]) cylinder(d=6, h=28);
        translate([40-3, 40-3, 0]) cylinder(d=6, h=28);
    }
    translate([20, 20, -1]) cylinder(d=38, h=42);
}
translate([20, 20, 0]) cylinder(d=12, h=28);
$fn=120;

translate([20, 20, 0])
linear_extrude(height = 28, center = false, convexity = 10, twist = 360, $fn = 100)
translate([5, 0, 0])
square([13, 1]);

translate([20, 20, 0]) rotate([0, 0, 120])
linear_extrude(height = 28, center = false, convexity = 10, twist = 360, $fn = 100)
translate([5, 0, 0])
square([13, 1]);

translate([20, 20, 0]) rotate([0, 0, 240])
linear_extrude(height = 28, center = false, convexity = 10, twist = 360, $fn = 100)
translate([5, 0, 0])
square([13, 1]);

}

module front_extension() {
    difference() {
    union() {
        cube([215, 190, 5]);
        cube([4, 190, 55]);
        cube([215, 4, 55]); 
        translate([215-4, 0, 0]) cube([4, 190, 55]);    
        translate([0, 190-4, 4]) cube([215, 4, 55-4]);
        translate([0, 190-15, 55-4]) cube([215, 15, 4]);
        }
    translate([15, 15, -1]) cube([215-2*15, 190-2*15, 7]);
    //cutout magnets
        translate([50, 190-6.5, 0]) cylinder(d1=9, d2=8.2, h=3.2);
        translate([215-50, 190-6.5, 0]) cylinder(d1=9, d2=8.2, h=3.2);
        translate([50, 190-6.5, 5-1.5]) cylinder(d=9, h=4);
        translate([215-50, 190-6.5, 5-1.5]) cylinder(d=9, h=4);
        
        translate([6.5, 50, 0]) cylinder(d1=9, d2=8.2, h=3.2);
        translate([215-6.5, 50, 0]) cylinder(d1=9, d2=8.2, h=3.2);
        translate([6.5, 50, 5-1.5]) cylinder(d=8.2, h=4);
        translate([215-6.5, 50, 5-1.5]) cylinder(d=8.2, h=4);
    }
}