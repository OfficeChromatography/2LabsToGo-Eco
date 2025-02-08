//x-cart

$fn=80;
d=11; // d pulley

x_axis_cart_tensioner();  //to be printed
//tensioner();  //to be printed

module x_axis_cart_tensioner() {
difference() {
    union() {
        translate([0, 1, 0]) cube([64.5, 26, 4.5]);
        translate([20, 20, 4.5]) cube([24.5, 10, 12]);      
    }
    translate([22.5, 27+3, 16.5-3]) rotate([90, 0, 0]) cylinder(d1=2.7, d2=2.4, h=10);
    translate([23-0.7, 15, 16.5-6]) cube([1.4, 16, 10]);
    translate([32.25+d/2-1.5, 15, 16.5-7]) cube([3, 16, 10]);
    
    translate([64.5-20, 2, 0]) cube([20, 24, 6]);
    translate([64.5-20-44.5, 2, 0]) cube([20, 24, 6]);
    translate([32.25-d/2-2, 28.5+3, 16.5-6]) rotate([0, 0, 270]) timing_belt();
    
    translate([32.25, 35, 10]) rotate([90, 0, 0]) cylinder(d=3.2, h=30);
    translate([32.25, 35+3, 10]) rotate([90, 0, 0]) cylinder(d=6.1, h=8+6, $fn=6);
    
    //holes for screws
    translate([64.5-22, 5.1, -1]) cylinder(d=2.7, h=10);
    translate([64.5-22, 27-4.1, -1]) cylinder(d=2.7, h=10);
    translate([64.5-22-20, 5.1, -1]) cylinder(d=2.7, h=10);
    translate([64.5-22-20, 27-4.1, -1]) cylinder(d=2.7, h=10);
    //cutout
    translate([26, 0, 8.5]) cube([8, 3, 10]);
}
translate([64.5-20, 1, 0]) bearing();
translate([64.5-20-44.5, 1, 0]) bearing();
pusher();
}

module bearing() {
difference() {
    cube([20, 26, 14]);
    translate([10, -1, 10]) rotate([-90, 0, 0]) cylinder(d=15, h=28);
    }
}

module timing_belt() {
difference() {
    cube([44, 2.0, 11,]);
    D=2;
    R=0.75;
    for (i=[0:16])
        translate([i*D+2.5, 2.0, -1]) cylinder(r=R, h=12, $fn=6);
}
}

module pusher() {
    difference() {
    translate([64.5-5, 28-1, 0]) cube([5, 18, 14]);
      translate([54.5, 26, 10]) rotate([-90, 0, 0]) cylinder(d=15, h=28);  
    }
}

module tensioner() {
difference() {
translate([20, 1, 4.5]) cube([24, 10, 12]);
    translate([32.25-d/2-2, 30.5, 16.5-6]) rotate([0, 0, -90]) timing_belt();
    translate([22.5, 11, 16.5-3]) rotate([90, 0, 0]) cylinder(d1=2.4, d2=2.7, h=10);
    translate([23-0.7, -5, 16.5-6]) cube([1.4, 17, 10]);
    translate([32.25+d/2-1.5, -5, 16.5-7]) cube([3, 26, 10]);
    translate([32.25, 25, 10]) rotate([90, 0, 0]) cylinder(d=3.2, h=30);
    translate([32.25, 4.5, 10]) rotate([90, 0, 0]) cylinder(d=5.9, h=30);
    }
}