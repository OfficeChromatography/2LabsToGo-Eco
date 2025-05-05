$fn=80;
distance=111;
d=11; // d pulley+timing belt
m=60; //Mitte

y_axis_cart();
//timing_belt();
//holder();
//translate([0, -5, 0]) tensioner();

module bearing() {
difference() {
    cube([20, 24.5, 14]);
    translate([10, -1, 10]) rotate([-90, 0, 0]) cylinder(d=15.5, h=26);
    }
}

module y_axis_cart() {
    difference() {
        union() {
            cube([120, 90, 7]);
            translate([0, 90, 0]) cube([120, 5, 4]);
            holder();            
        }
        //holes for plate holder screws
        translate([20, 21.5, -1]) cylinder(r=5.8, h=4.5);
        translate([120-20, 21.5, -1]) cylinder(r=5.8, h=4.5);
        translate([20, 95-8.5, -1]) cylinder(r=5.8, h=4.5);
    translate([120-20, 95-8.5, -1]) cylinder(r=5.8, h=4.5);
        
        //screw for tensioneer
            translate([60+15, 59, -1]) rotate([0, 0, 0]) cylinder(d=2.7, h=20);
        //cutout for bearings
        translate([12, 56, 4]) cube([20, 24.5, 4]);
        translate([12+76, 56, 4]) cube([20, 24.5, 4]);
        //cutout for M4 screw fitting to the positioning holes of the plate holder
        translate([4.5, 68, -1]) cylinder(r=2.0, h=12);
        translate([4.5+distance, 68, -1]) cylinder(r=2.0, h=12);
        //cutout pulley
        translate([60-25/2, -1, 1]) cube([25, 25, 7]);
        //cutout screw endstop
        translate([120-8-8, 90+5-3.6, 1.5])  cube([8, 5, 3]); 
        
        //cutout magnets
        translate([4, 22+8.1/2, 3.5]) cube([9, 8.1, 3], center=true);
        translate([4, 79.9+8.1/2, 3.5]) cube([9, 8.1, 3], center=true);
        translate([120-4, 22+8.1/2, 3.5]) cube([10, 8.1, 3], center=true);
        translate([120-4, 79.9+8.1/2, 3.5]) cube([10, 8.1, 3], center=true);
        //cutout timing belt
        //translate([55, 24+43.25, 7]) rotate([0, 0, -90]) timing_belt();
        
    string="100.5%";
    translate([85, 20, 6.5])     linear_extrude(2.0) text(string, size = 6, direction = "ltr", spacing = 1 );
    }
    difference() {
        union() {
    translate([12, 56, 2]) bearing();
    translate([12+76, 56, 2]) bearing();
    }
    //holes for plate holder screws
    translate([20, 95-8.5, -1]) cylinder(r=5.8, h=4.5);
    translate([120-20, 95-8.5, -1]) cylinder(r=5.8, h=4.5);
}
    //tip for endstop
    translate([120-12, 90-10, 7]) cube([12, 10, 12]);
}

module holder() {
difference() {
translate([51, 24, 0]) cube([25, 20, 15]);
    translate([m-d/2, 28+23.1, 9]) rotate([0, 0, -90]) timing_belt();
    translate([m-d/2, 24, 9]) cube([3, 3.2, 10]);
    translate([58.5, 44, 13]) rotate([90, 0, 0]) cylinder(d1=2.3, d2=2.7, h=17);
    translate([58.5, 27, 13]) rotate([90, 0, 0]) cylinder(d=5.6, h=10);
    translate([58.5-0.7, 20, 11-1]) cube([1.4, 26, 10]);
    translate([m+d/2, 20, 11-4]) cube([2.5, 26, 10]);
    
    translate([60+12, 44-4, 11]) rotate([90, 0, 0]) cylinder(d=6.3, h=25, $fn=6);
    translate([60+12, 44+2, 11]) rotate([90, 0, 0]) cylinder(d=3.3, h=30);
}
}

module tensioner() {
difference() {
translate([51, 54, 7]) cube([30, 20, 15-7]);
    translate([m-d/2, 24+53, 9]) rotate([0, 0, -90]) timing_belt();
    translate([58.5, 50+24, 13]) rotate([90, 0, 0]) cylinder(d1=2.7, d2=2.3, h=20);
    //translate([58.5, 27+54, 12.5]) rotate([90, 0, 0]) cylinder(d=5.6, h=10);
    translate([58.5-0.7, 20+30, 11-1]) cube([1.4, 26, 10]);
    translate([m+d/2, 20+30, 11-2]) cube([2.5, 26, 10]);
    translate([60+12, 50+30, 11]) rotate([90, 0, 0]) cylinder(d=3.3, h=30);
    
    hull() {
    translate([60+15, 60, 5]) rotate([0, 0, 0]) cylinder(d=3.3, h=15);
    translate([60+15, 68, 5]) rotate([0, 0, 0]) cylinder(d=3.3, h=15);
    }
    }
}

module timing_belt() {
difference() {
    cube([24, 1.9, 7,]);
    D=2;
    R=0.75;
    for (i=[0:16])
        translate([i*D+2, 1.9, -1]) cylinder(r=R, h=12, $fn=6);
}
}
