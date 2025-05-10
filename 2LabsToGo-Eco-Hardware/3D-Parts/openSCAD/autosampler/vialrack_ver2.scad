//your vial data, correct respectively
d=11;  //vial OD plus 0.5 mm
d1=13; //vial cap OD + 0.5 mm
h=42.2;  //vial height including cap plus 0.5 mm
n=8;  //number of sample vials without rinsing vial
p=8;  //spindle pitch

$fn=80;

b=6;

vial_rack();
//test vial
//color("white", 0.6) {translate([10, 10, 3-2]) cylinder(d=d, h=h); 
    //translate([10, 10, 3+h-3]) cylinder(d=d1, h=3);
    //}

//color("blue", 1.9) { translate([58, 9.5, -2]) import("vialrack_holder.stl"); }

//poly();

module vial_rack() {
difference(){
    D=4.5;
union() {
difference() {
    cube([116, 20, 40]);
    //cut bottom
    //translate([-2, -7, -6]) cube([160, 40, 8]); 
    
    //Screw holes/slit
    translate([20+4.5, 20-D, -3]) cylinder(d=6.5, h=6);
    translate([20+10, 20-D, -3]) cylinder(d=6.5, h=6);
    translate([20+4.5, 20-D-6.5/2, -3]) cube([5.1, 6.5, 6]);    
    
    translate([20+14.5, D, -3]) cylinder(d=6.5, h=6);
    translate([20+14.5+5.1, D, -3]) cylinder(d=6.5, h=6);
    translate([20+14.5, D-6.5/2, -3]) cube([5.1, 6.5, 6]);
    
    translate([20+5+70, 20-D, -3]) cylinder(d=6.5, h=6);
    translate([20+5+70+5.1, 20-D, -3]) cylinder(d=6.5, h=6);
    translate([20+5+70, 20-D-6.5/2, -3]) cube([5.1, 6.5, 6]);
    
    translate([20+1.5+84, D, -3]) cylinder(d=6.5, h=6);
    translate([20+1.5+84+5.1, D, -3]) cylinder(d=6.5, h=6);
    translate([20+1.5+84, D-6.5/2, -3]) cube([5.1, 6.5, 6]);
          
    //cutout vials
    for(x = [10 : 14: 14*n-4])
    translate([x, 10, 1+b+2]) cylinder(d=d, h=h-4);
    //for(z = [10 : 14: 14*n-4])
    //translate([z-d/2, 10, 1+b+2]) cube([d, d, 35]);
    
    //cutout oben Anschlag
    /*for(c = [10 : 14: 14*n-4])
    translate([c-d1/2, -2, h-7+6-2+b+2]) cube([d1, 24, 2]);
    for(f = [10 : 14: 14*n-4])
    translate([f-d/2, -2, 30-2+b]) cube([d, 24, 11.5]);
    for(g = [10 : 14: 14*n-4])
    translate([g, 10, -1]) cylinder(d=5, h=12);
    */
    //cutout back view
    for(f = [10 : 14: 14*n-4])
    translate([f-2.5-0.25, -7, 5-2+4+2]) cube([5.5, 30, 30-4.75]);
    
    
    //cutout rounding the walls
    for(f = [10 : 14: 14*n-4])
    translate([f-d/2+d/2, -7, 30-2+b]) rotate([-90, 0, 0]) cylinder(d=5.5, h=30);
    /*
    for(f = [10 : 14: 14*n-4])
    //translate([f, -7, h-7+6-2+b+2]) rotate([-90, 0, 0]) cylinder(d=d1, h=30, $fn=6);
    for(f = [10 : 14: 14*n-4])
    translate([f, -7, h-7+6-2+b+2]) rotate([-90, 0, 0]) cylinder(d=d1, h=30, $fn=6);
    
    for(f = [10 : 14: 14*n-4])
    //translate([f, -7, h+1-2+b]) rotate([-90, 0, 0]) cylinder(d=d1, h=30, $fn=6);
    //#translate([f, -7, h+1-2+b]) poly();
    
    for(c = [10 : 14: 14*n-4])
    translate([c-d1/2, 21, 49.2]) poly();
    //translate([17.5, 21, 49.2]) poly();
    //c-d1/2, -2, h-7+6-2+b
    */
    //holes for the needle
    //for(a = [10 : 14: 14*n-4])
    //translate([a, 10, 46]) cylinder(d=8, h=15);
    for(g = [10 : 14: 14*n-4])
    translate([g, 10, -1]) cylinder(d=5, h=12);
}
//body rinsing vial
difference() {
    translate([116, -6, 0]) cube([35, 32, 45]);
    //translate([-1, -7, -6]) cube([160, 35, 8]); 
    //cutout bottom for vial
    //#translate([133, 10, 3-2]) cylinder(d=30, h=50);
    translate([133, 10, 3-2]) cylinder(d=31, h=60);
    //translate([133-31/2, 10, 10]) cube([31, 18, 60]);
    //cutout top vial
    //#translate([133, 10, 56-12]) cylinder(d=30, h=7);
    //translate([133-30/2, 10, 56-10]) cube([30, 18, 7-2]);
    //translate([133-30/2, -9, 10]) cube([30, 36, 36]);
    //translate([132-5, -9, 1]) cube([10, 36, 35]);
    
    //hole for needle rinsing vial
    //translate([133, 10, 39]) cylinder(d=20, h=20);
    translate([133-10, -10, 10]) cube([20, 40, 45]);
    }
}
//translate([-1, -6, 48.6])cube([131.36, 9, 8]);
}
//support for positioning
translate([-2, 5, 0]) cube([3, 10, 2]);
//translate([150, 10, 23]) sphere(d=3.4);
translate([150, 0, 20]) cube([3, 20, 2]);
}

module poly() {
    rotate([90, 0, 0])
    linear_extrude(height = 22, scale = 1)
    
    polygon([[0,0],[3.25,5.629-1.5], [13-3.25,5.629-1.5], [13,0]]);
    //polygon([[0,0],[100,0],[130,50],[30,50]],[[1,0,3,2]]);
}