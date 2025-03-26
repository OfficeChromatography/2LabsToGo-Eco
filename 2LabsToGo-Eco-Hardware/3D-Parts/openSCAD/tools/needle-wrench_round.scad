//needle wrench

difference()  {
    cylinder(d=20, h=5, $fn=8);
    translate([-4.2/2, -4.2/2, -1]) cube([4.2, 4.2, 7]);
    translate([-0.75, 0, -1]) cube([1.5, 20, 7]);
}