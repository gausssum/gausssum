#include "colors.inc"
#include "textures.inc"
#include "metals.inc"
#include "finish.inc"
#include "skies.inc"
#include "mesh2.inc"

camera {
    location <.5, 1.5, -2>    look_at <0, 0, 0>
}

light_source { <50, 50, -50> color rgb<1, 1, 1> }
light_source { 
    < 2, 9, -3> 
    color White 
    area_light <2,0,0>,<0,0,2>, 2, 2
    adaptive 1
    jitter
}


  sky_sphere {
    pigment {
      gradient y
      color_map {
        [0.000 0.002 color rgb <1.0, 0.2, 0.0>
                     color rgb <1.0, 0.2, 0.0>]
        [0.002 0.200 color rgb <0.8, 0.1, 0.0>
                     color rgb <0.2, 0.2, 0.3>]
      }
      scale 2
      translate -1
    }
    pigment {
      bozo
      turbulence 0.65
      octaves 6
      omega 0.7
      lambda 2
      color_map {
          [0.0 0.1 color rgb <0.85, 0.85, 0.85>
                   color rgb <0.75, 0.75, 0.75>]
          [0.1 0.5 color rgb <0.75, 0.75, 0.75>
                   color rgbt <1, 1, 1, 1>]
          [0.5 1.0 color rgbt <1, 1, 1, 1>
                   color rgbt <1, 1, 1, 1>]
      }
      scale <0.2, 0.5, 0.2>
    }
    rotate -135*x
  }

plane { <0, 1, 0>, -1
	texture {   
		pigment { 
			checker color Black, color White 
		}
		finish {Phong_Glossy}
	}
}

object { pov_curve 

 pigment { BrightGold }
     finish {
        ambient .1
        diffuse .1
        specular 1
        roughness .01
        metallic
        reflection {
          .65
          metallic
        }
     }


}

	


