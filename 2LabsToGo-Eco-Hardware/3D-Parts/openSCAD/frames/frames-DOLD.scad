//frames

$fn=80;
y1=102;
y2=148;
x=215;
z=210;
b=13;
pd=6.3; //profile depth

//right_front();
//right_back();
//left_front();
//left_back();
back();
//top_front();
//top_front_fan();
//top_back();
//top_back_cable_channel();
//top_back_cover();
//board_cover();
//translate([55, 13, 12.5]) board_cover(); 
//front();
//cover_z_motor();
//cable_clip_1();
//cable_clip_2();
//cable_clip_3();
//cable_clip_alu();
//color("blue", 0.5) {rotate([-90, 0, 90]) translate([8, -15, -80]) cable_support();} //electronic box
//cable_support();
//translate([202, 10, 14.5]) rotate([0, 180, 0]) cable_support();
//scratching_aid_magnets_front();

//bohrschablone();

module top_front_fan() {
difference() {
import("frame_top_front.stl");
    translate([71.75-0.5, 7.5, -1]) cube([81, 80, 10]);
}
}


module bohrschablone() {
    w=y1+2*pd;
    h=z+2*pd;
    difference() {
        translate([-5, -5, 0])cube([230, 130, 8]);
        translate([0, 0, 5]) cube([260, 130, 5]);
        
        n1=(h-2*pd)/2-6;  //h-2*pd = y1 or y2
        n2=(w-2*pd)/2-6;
        
        for (i=[0:2])
        translate([6, 6+i*n1, -4]) cylinder(d=3.2, h=10);
        for (i=[0:2])
        translate([w-2*pd-6, 6+i*n1, -4]) cylinder(d=3.2, h=10);
        for (i=[0:2])
        translate([6+i*n2, 6, -4]) cylinder(d=3.2, h=10); 
        //for (i=[0:2])
        //translate([6+i*n2, h-2*pd-6, -4]) cylinder(d=2.9, h=10); 
        
    w=y2+2*pd;
    h=z+2*pd;
    n3=(h-2*pd)/2-6;  //h-2*pd = y1 or y2
    n4=(w-2*pd)/2-6;
        for (i=[0:2]) //links
        translate([6, 6+i*n3, -4]) cylinder(d=3.2, h=10);
        for (i=[0:2])  //rechts
        translate([w-2*pd-6, 6+i*n3, -4]) cylinder(d=3.2, h=10);
        for (i=[0:2])  //unten
        translate([6+i*n4, 6, -4]) cylinder(d=3.2, h=10); 
        //for (i=[0:2])  //oben
        //translate([6+i*n2, h-2*pd-6, -4]) cylinder(d=2.9, h=10);
    //h=z+2*pd-20;
    w1=x+2*pd;
    n5=(h-2*pd)/2-6;  //h-2*pd = y1 or y2
    n6=(w1-2*pd)/2-6; 
        for (i=[0:2]) //links
        translate([6, 6+i*n5, -4]) cylinder(d=3.2, h=10);
        for (i=[0:2])  //rechts
        translate([w1-2*pd-6, 6+i*n5, -4]) cylinder(d=3.2, h=10);
        for (i=[0:2])  //unten
        translate([6+i*n6, 6, -4]) cylinder(d=3.2, h=10); 
    }
}

module frame(w, h, d) {
    difference() {
        translate([-pd, -pd, 0]) cube([w, h, d]);
        translate([b, b, -4]) cube([w-2*pd-2*b, h-2*pd-2*b, 12]);
        //cutout edges
        translate([-pd, -pd, -1]) cube([pd+2.2, pd, 8]);
        translate([-pd, -pd, -1]) cube([pd, pd+2.2, 8]);
        translate([w-2*pd-2.2, -pd, -1]) cube([pd+2.2, pd, 8]);
        translate([w-2*pd, -pd, -1]) cube([pd, pd+2.2, 8]);
        translate([w-2*pd-2.2, h-2*pd, -1]) cube([pd+2.2, pd, 8]);
        translate([w-2*pd, h-2*pd-2.2, -1]) cube([pd, pd+2.2, 8]);
        
        translate([-pd, h-2*pd-2.2, -1]) cube([pd, pd+2.2, 8]);
        translate([-pd, h-2*pd, -1]) cube([pd+2.2, pd, 8]);
    //holes for screws
    n1=(h-2*pd)/2-6;  //h-2*pd = y1 or y2
    n2=(w-2*pd)/2-6;  //w-2*pd = x
    for (i=[0:2])
        translate([6, 6+i*n1, -4]) cylinder(d=2.9, h=10);
    for (i=[0:2])
        translate([w-2*pd-6, 6+i*n1, -4]) cylinder(d=2.9, h=10);
    for (i=[0:2])
        translate([6+i*n2, 6, -4]) cylinder(d=2.9, h=10); 
    for (i=[0:2])
        translate([6+i*n2, h-2*pd-6, -4]) cylinder(d=2.9, h=10);
    }
} 

module left_front() {  //korrigiert
    frame(y1+2*pd, z+2*pd, 5);
    //cable channel
    translate([b-4, b, 5]) cube([4, z-2*b, 7.5]);
    translate([b-4, z-b, 5]) cube([y1-2*b+4, 4, 7.5]);
    //translate([y1-b, b-4, 5]) cube([4, z-2*b+4+4, 7.5]);
    //translate([b-4, b-4, 5]) cube([y1-2*b+4, 4, 7.5]);
    string1 = str("left-front");
    translate ([10, 3, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
}

module right_front() {   //korrigiert
    frame(y1+2*pd, z+2*pd, 5);
    //cable channel
    translate([y1-b, b-4, 5]) cube([4, z-2*b+4+4, 7.5]);
    translate([b-4, z-b, 5]) cube([y1-2*b+4+4, 4, 7.5]);
    translate([b-4, 155, 5]) cube([4, 46, 7.5]);
    string1 = str("right-front");
    translate ([10, 3, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
}

module right_back() {  //okay
    frame(y2+2*pd, z+2*pd, 5);
    string1 = str("right-back");
    translate ([10, 3, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
}

module left_back() {
    frame(y2+2*pd, z+2*pd, 5);
    //cable channel
    translate([y2-b, b-4, 5]) cube([4, z-2*b+4+4, 7.5]);
    //translate([b-4, b-4, 5]) cube([4, z-2*b+4+4, 7.5]);
    translate([b, z-b, 5]) cube([y2-2*b, 4, 7.5]);
    //translate([b-4, b-4, 5]) cube([y2-2*b+4, 4, 7.5]);
    string1 = str("left-back");
    translate ([10, 3, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
}

module back() {  
    difference() {
        union() {
        frame(x+2*pd, z+2*pd-20, 5);
        translate([0, 0, -2.5]) cube([x, z-20, 3]);
            //cable channel
    translate([b, b-4, 5]) cube([130, 4, 7.5-2]);
        }
        //cutout bottom
        translate([-10, -8, -4]) cube([240, 8, 10]);
        //cutout center
        translate([b, b, -4]) cube([(x+2*pd)-2*pd-2*b, (z+2*pd-20)-2*pd-2*b, 12]);
        //cutout camera tower holder
        translate([-10, 20+1, -4]) cube([250, 110, 10]);
        //cutout spindle
        translate([x-32.5, 5.1, -3]) cylinder(d=8.2, h=10);
        translate([x-32.5-8.2/2, -1, -3]) cube([8.2, 6.1, 10]);
        //cutout rack-holder
        translate([x-49.5, 9.3, 0]) cube([32, 4, 7.5]);
        //cutout motor cable
        translate([x-35-32, 3, -3]) cylinder(d=4, h=10);
        translate([x-35-32-4/2, -1, -3]) cube([4, 4, 10]); 
    //holes for screws
    h=z+2*pd-20;
    w=x+2*pd;
    n1=(h-2*pd)/2-6;  //h-2*pd = y1 or y2
    n2=(w-2*pd)/2-6;  //w-2*pd = x
    for (i=[0:2])
        translate([6, 6+i*n1, -4]) cylinder(d=2.8, h=12);
    for (i=[0:2])
        translate([w-2*pd-6, 6+i*n1, -4]) cylinder(d=2.8, h=12);
    for (i=[0:2])
        translate([6+i*n2, 6, -4]) cylinder(d=2.8, h=12); 
    for (i=[0:2])
        translate([6+i*n2, h-2*pd-6, -4]) cylinder(d=2.8, h=12);
    
    //additional holes for rF-box
    translate([58, 6, -4]) cylinder(d=2.8, h=12);
    translate([54, 184, -4]) cylinder(d=2.8, h=12);
    
    
    //cut in 2 parts: -10 to 100, 100 to 230
        //translate([100, -10, -5]) cube([130, 250, 20]);
    string1 = str("top-back");
    translate ([160, 185, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
    string2 = str("bottom-back");
    translate ([15, 3, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string2, size = 6, direction = "ltr", spacing = 1 );
        }
    //cable channel
    //translate([b, b-4, 5]) cube([130, 4, 7.5]);
     //test camera-holder
     //translate([0, 20, 0]) import("camera-holder-90Grad.stl");
     //translate([0, 95, 0]) cylinder(d=2.9, h=10);   
        w=x+2*pd;
    translate([-pd, 0, 0]) cube([pd+2, 6, 5]);
    translate([w-2*pd-2, 0, 0]) cube([pd+2, 6, 5]);
        //([w-2*pd-2, -pd, -1])
}

module top_front() {
    frame(x+2*pd, y1+2*pd, 5);
    //testing panel
    //translate([0, 0, 3]) import("panels_top-front.stl");
    string1 = str("top-front");
    translate ([20, 3, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
    difference() {
        translate([b, 89, 5]) cube([189, 7, 7]);
        //translate([b-1, 90, 5]) rotate([45, 0, 0]) cube([191, 11, 7]);
        translate([b-1, 90-1, 5]) rotate([45, 0, 0]) cube([191, 11, 7]);
    }
}

module top_back() {
    difference()  {
        frame(x+2*pd, y2+2*pd, 5);
        //srew hole top connector e-axis
        translate([215-5, y2-74.55, -1]) cylinder(d=3.9, h =10);
        string1 = str("top-back ↑");
    translate ([80, 140, 2]) rotate([0, 180, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
        //cut for testing
        //translate([-10, -10, -2]) cube([200, 180, 10]);
    }
}

module frame_electronic_box(w, h, d) {
    difference() {
        translate([-pd, -pd, 0]) cube([w, h, d]);
        translate([b, b, -4]) cube([w-2*pd-2*b, h-2*pd-2*b, 12]);
        //cutout edges
        translate([-pd, -pd, -1]) cube([pd+2, pd, 8]);
        translate([-pd, -pd, -1]) cube([pd, pd+2, 8]);
        translate([w-2*pd-2, -pd, -1]) cube([pd+2, pd, 8]);
        translate([w-2*pd, -pd, -1]) cube([pd, pd+2, 8]);
        translate([w-2*pd-2, h-2*pd, -1]) cube([pd+2, pd, 8]);
        translate([w-2*pd, h-2*pd-2, -1]) cube([pd, pd+2, 8]);
        
        translate([-pd, h-2*pd-2, -1]) cube([pd, pd+2, 8]);
        translate([-pd, h-2*pd, -1]) cube([pd+2, pd, 8]);
        
    //holes for screws
    /*n1=(h-2*pd)/2-6;  //h-2*pd = y1 or y2
    n2=(w-2*pd)/2-6;  //w-2*pd = x
    for (i=[0:2])
        translate([6, 6+i*n1, -4]) cylinder(d=3.3, h=10);
    for (i=[0:2])
        translate([w-2*pd-6, 6+i*n1, -4]) cylinder(d=3.3, h=10);
    */
    translate([6, y2-20, -2]) cylinder(d=3.3, h=15);
    translate([6, y2-70, -2]) cylinder(d=3.3, h=15);
    translate([w-2*pd-5.5, 30, -2]) cylinder(d=3.3, h=15);
    translate([w-2*pd-5.5, y2-40, -2]) cylinder(d=3.3, h=15);
    }
} 

module top_back_cable_channel() {
    difference()  {
        union() {
        frame_electronic_box(x+2*pd, y2+2*pd, 5);
            translate([13, 13, 0]) cube([10, 128, 5]);
        }
        //cutout bracket e-axis top
        translate([-7, 40, -1]) cube([22, 22, 8]);
        //cutout for e-motor
        translate([19, 28, -1]) cube([6, 46, 8]); 
        
        string1 = str("top-back ↑");
        translate ([140, 140, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
    }
    //cable channel
    difference() {
        union() {
    translate([18, b-4, 5]) cube([x-b-13-4-5, 4, 7.5]);
    translate([13, y2-b, 5]) cube([x-b-13-4, 4, 7.5]);
        }
        translate([212-70-5, 0, 5+7.5-4.5]) rotate([-90, 0, 0]) cylinder(d=2.7, h=150);
    }
    
}

module top_back_cover() {
    difference()  {
        frame(x+2*pd, y2+2*pd, 5);
        //srew hole top connector e-axis
        //translate([215-5, y2-74.55, -1]) cylinder(d=3.9, h =10);
        
        //cutout bracket e-axis top
        translate([-7, 41, -1]) cube([22, 20, 8]);
        //cut for testing
        //translate([-10, -10, -2]) cube([200, 180, 10]);
        string1 = str("top-back ↑");
        translate ([140, 140, 4]) rotate([0, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
        holes_2();
    }
    //cable channel
    //translate([13, b-4, 5]) cube([x-b-13-4, 4, 7.5]);
    
    //support for board_cover
    difference() {
        union() {
        translate([13, b-5, 5]) cube([x-b-13, 5, 27]);
        translate([13, y2-13, 5]) cube([x-b-13, 5, 27]);   
        }
        translate([10-1, b-4+4, 27.5]) rotate([0, 90, 0]) cylinder(d=5, h=x-b-13+8);
        translate([10-1, y2-13, 27.5]) rotate([0, 90, 0]) cylinder(d=5, h=x-b-13+8);
    }
    //cube([13, 15, 25]);
    translate([b, b, 0]) cube([3, y2-b, 5]);
}

module board_cover() {
    cube([150, 122, 4.8]);
    rotate([0, 90, 0]) translate([-4.8/2, 0, 0]) cylinder(d=4.8, h=150);
    rotate([0, 90, 0]) translate([-4.8/2, 122, 0]) cylinder(d=4.8, h=150);
}


module holes_2() {
//holes for screws top_back_cover 3.2 mm
    h=y2+2*pd;
    w=x+2*pd;
    n1=(h-2*pd)/2-6;  //h-2*pd = y1 or y2
    n2=(w-2*pd)/2-6;  //w-2*pd = x
    for (i=[0:2])
        translate([6, 6+i*n1, -4]) cylinder(d=3.2, h=10);
    for (i=[0:2])
        translate([w-2*pd-6, 6+i*n1, -4]) cylinder(d=3.2, h=10);
    for (i=[0:2])
        translate([6+i*n2, 6, -4]) cylinder(d=3.2, h=10); 
    for (i=[0:2])
        translate([6+i*n2, h-2*pd-6, -4]) cylinder(d=3.2, h=10);
}

module front() {
    difference() {
        union() {
        frame(x+2*pd, z+2*pd-20, 5);
        cube([x, z-20, 7]);
        }
        translate([-10, -7, -1]) cube([230, 7, 8]);
        translate([b, b, -1]) cube([x-2*b, z-20-2*b, 14]);
        //cutout plate holder
        translate([26, 5, -1]) cube([176, 9, 10]);
        //cutout screw
        translate([92, -2, 0]) rotate([-90, 0, 0]) cylinder(d=6, h=10);
        //cutout magnets
        translate([50, 184,-1]) cylinder(d=8.2, h=4);
        translate([215-50, 184,-1]) cylinder(d=8.2, h=4);
        translate([50, 184, 7-3]) cylinder(d=9, h=4);
        translate([215-50, 184, 7-3]) cylinder(d=9, h=4);
        //cutout endstop connector
        translate([220-6-5, -1, -1]) cube([15, 10, 3.5]);
        //cutout vial-rack-holder
        translate([201, 5, -1]) cube([4, 12, 10]);
    }
    difference() {
        translate([92+60, 0, -6]) cube([16, 5, 6]);
        translate([92+66, -2, -5]) rotate([-90, 0, 0]) cylinder(d=6, h=10);
    }
}

module holes() {
    for (i=[1:6])
        translate([-10, -28+i*40, -1]) slit_y();  //y
    //for (i=[1:6])
        //translate([215+10, -150+i*40, -1]) slit_y();  //y
    //for (i=[1:7])
        //translate([i*30-14, 135+10, -1]) slit_x();  //x
    //for (i=[1:7])
        //translate([i*30-14, -135-10, -1]) slit_x();  //x
    //holes for legs
    //translate([4*30-14, -135-10, -1]) cylinder(d=5.2, h=10); //front
    //translate([-10.5, 110+8, -1]) cylinder(d=5.2, h=10);   //back
    //translate([215+10, -130+8*30+8, -1]) cylinder(d=5.2, h=10); //back    
}

module slit_x() {
    hull()  {
        cylinder(d=3.2, h=5);
        translate([8, 0, 0]) cylinder(d=3.2, h=5);
    }
}

module slit_y() {
    hull()  {
        cylinder(d=3.2, h=5);
        translate([0, 8, 0]) cylinder(d=3.2, h=5);
    }
}

module cover_z_motor() {
    difference() {
        union() {
            cube([46, 10, 28]);
            translate([-5, 0, 0]) cube([46+5+5, 2, 28+5]);
        }
        translate([2, -2, -2]) cube([42, 20, 28]);

    //hole for screw panel mounting
    translate([46+5-1.5, -1, 6]) rotate([-90, 0, 0]) cylinder(d=6, h=5);
    }
}

module cable_clip_1() {
    h1=20; //length
    difference() {
        union() {
    cube([20, 2, h1]);
    translate([0, 0, 0]) cube([1, 7, h1]);
    translate([5, 0, 0]) cube([1, 7, h1]);
    translate([5, 5, 0]) cylinder(d=0.8, h=h1);
        }
        translate([1.4, 5.5, -1]) rotate([0, 0, 45]) cube([2, 2, h1+2]);
        translate([3.6, 7.4, -1]) rotate([0, 0, -45]) cube([2, 2, h1+2]);
        string1 = str("1");
    translate ([7, 1.5, 4]) rotate([90, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
    }
}

module cable_clip_2() {
    h1=20; //length
    difference() {
        union() {
    cube([16, 2, h1]);
    translate([0, 0, 0]) cube([1, 7, h1]);
    translate([5, 0, 0]) cube([1, 7, h1]);
    translate([5, 5, 0]) cylinder(d=0.8, h=h1);
        }
        translate([1.4, 5.5, -1]) rotate([0, 0, 45]) cube([2, 2, h1+2]);
        translate([3.6, 7.4, -1]) rotate([0, 0, -45]) cube([2, 2, h1+2]);
        string1 = str("2");
    translate ([7, 1.5, 4]) rotate([90, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
    }
}

module cable_clip_3() {
    h1=20; //length
    difference() {
        union() {
    cube([13, 2, h1]);
    translate([0, 0, 0]) cube([1, 7, h1]);
    translate([5, 0, 0]) cube([1, 7, h1]);
    translate([5, 5, 0]) cylinder(d=0.8, h=h1);
        }
        translate([1.4, 5.5, -1]) rotate([0, 0, 45]) cube([2, 2, h1+2]);
        translate([3.45, 7.4, -1]) rotate([0, 0, -45]) cube([2, 2, h1+2]);
        string1 = str("3");
    translate ([4, 1.5, 4]) rotate([90, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
    }
}

module cable_clip_alu() {
    h1=20; //length
    difference() {
        union() {
    cube([16, 2, h1]);
    translate([5.25, 0, 0]) cube([1, 6, h1]);
    translate([16-5.25-1, 0, 0]) cube([1, 6, h1]);
    translate([5.25, 4, 0]) cylinder(d=0.5, h=h1);
    translate([16-5.25, 4, 0]) cylinder(d=0.5, h=h1);       
            }
        translate([6.25, 5, -1]) rotate([0, 0, 45]) cube([2, 2, h1+2]);
        translate([16-5.25-1, 5, -1]) rotate([0, 0, 45]) cube([2, 2, h1+2]);
    string1 = str("alu");
    translate ([3, 1, 4]) rotate([90, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
    }
}

module cable_support_old() {
    h1=50; //length
    difference() {
        union() {
            cube([10, 3, h1]);
            //translate([5, 0, 0]) cube([5, 18, h1]);
            translate([6, 0, 0]) cube([122+4, 3, h1]);
            //translate([122+3, 12, 0]) cube([5, 7, h1]);
            translate([0, 0, 0]) cube([1, 7+2, h1]);
            translate([5, 0, 0]) cube([1, 7+2, h1]);
            translate([5, 5+2, 0]) cylinder(d=0.8, h=h1);
            translate([122+4, 0, 0]) cube([1, 7+2, h1]);
            translate([5+122+4, 0, 0]) cube([1, 7+2, h1]);
            translate([5+122+4, 5+2, 0]) cylinder(d=0.8, h=h1);
        }
            translate([1.4, 5.5+2, -1]) rotate([0, 0, 45]) cube([2, 2, h1+2]);
            translate([3.6, 7.4+2, -1]) rotate([0, 0, -45]) cube([2, 2, h1+2]);
            translate([1.4+122+4, 5.5+2, -1]) rotate([0, 0, 45]) cube([2, 2, h1+2]);
            translate([3.6+122+4, 7.4+2, -1]) rotate([0, 0, -45]) cube([2, 2, h1+2]);
            //translate([122+5, 13, -1]) cube([5, 5, h1+2]);
    string1 = str("cable support");
    translate ([20, 1, 3]) rotate([90, 0, 0])
    linear_extrude(2.0) text(string1, size = 6, direction = "ltr", spacing = 1 );
    }
    //translate([6, 10, 0]) cube([118, 3, 10]);
}

module cable_support()  {
    B=122+10+10;
    difference() {
        union() {
    translate([0, 0, 0]) cube([130, 136, 2]);
    //translate([0, -10, 2]) cube([130, 3, 7]);
    translate([0, 7, 2]) cube([130, 3, 7]);
    translate([0, 0, 2]) cube([130, 3, 7]);
    translate([0, 136-3, 2]) cube([130, 3, 7]);
    translate([0, 136-3-4-3, 2]) cube([130, 3, 7]);
    //translate([0, -10, 0]) cube([130, 7, 2]);
        }
        //hole for cables+plug
        translate([75, 11, -1]) cube([15, 15, 6]);
        //translate([85, 15, -1]) cylinder(d=10, h=6);
        //holes for mounting
        translate([60, 10, 6.5]) rotate([90, 0, 0]) cylinder(d=3.2, h=20);
        translate([60, 140, 6.5]) rotate([90, 0, 0]) cylinder(d=3.2, h=20);
    }
}

module scratching_aid_magnets_front() {
    difference() {
        cube([215+10, 50+5, 6]);
        translate([5, -1, 3]) cube([215, 51, 4]);
        translate([50+5, 50-6.5,-1]) cylinder(d=8.2, h=7);
        translate([165+5, 50-6.5,-1]) cylinder(d=8.2, h=7);
    }
    //cutout magnets
        //translate([50, 184,-1]) cylinder(d=8.2, h=4);
        //translate([215-50, 184,-1]) cylinder(d=8.2, h=4);
}