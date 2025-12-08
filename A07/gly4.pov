//Four glycine molecules at square vertices
#include "colors.inc"

light_source { <10, 10, -20> color White }
light_source { <-10, 5, -15> color Gray50 }
background { color Gray90 }

camera {
  location <0, 8, -20>
  look_at <0, 0, 0>
  right x*image_width/image_height
}

#include "glycine.pov"

object { mol_0 translate <3, 0, 3> }
object { mol_0 translate <-3, 0, 3> }
object { mol_0 translate <-3, 0, -3> }
object { mol_0 translate <3, 0, -3> }
