#include <stdio.h>
#include <math.h>

#define X_MIN -1
#define X_MAX 1
#define Y_MIN -1
#define Y_MAX 1
#define X_STEP_SIZE 0.007
#define Y_STEP_SIZE 0.007


/* POVRAY coordinates are left-handed:
 *   Y^  Z
 *    | /
 *    |/
 *    ----> X
 *
 *  
 *  
 *  */

float z_func (float x, float y );

int main(void){

	float i, j;

	struct coordinate {
			float x;
			float y;
			float z;
	};

	struct triangle {
			struct coordinate p1;
			struct coordinate p2;
			struct coordinate p3;
	} A, B;
	
	printf ("#declare pov_curve=mesh{\n");
	for	(i=X_MIN; i < X_MAX; i+=X_STEP_SIZE) {
		for	(j=Y_MIN; j < Y_MAX; j+=Y_STEP_SIZE) {
			
			A.p1.x = i;
			A.p1.y = z_func( i, j);
			A.p1.z = j;

			A.p3.x = i + X_STEP_SIZE;
			A.p3.y = z_func( i + X_STEP_SIZE, j);
			A.p3.z = j; 

			A.p2.x = i + X_STEP_SIZE;
			A.p2.y = z_func( i + X_STEP_SIZE, j + Y_STEP_SIZE );
			A.p2.z = j + Y_STEP_SIZE;

			printf ("triangle {\n");
			printf ("\t<%4.4f, %4.4f, %4.4f>,", A.p1.x, A.p1.y, A.p1.z);
			printf ("<%4.4f, %4.4f, %4.4f>,", A.p2.x, A.p2.y, A.p2.z);
			printf ("<%4.4f, %4.4f, %4.4f>\n", A.p3.x, A.p3.y, A.p3.z);
			printf ("}\n");

			B.p1.x = i;
			B.p1.y = z_func( i, j);
			B.p1.z = j;

			B.p3.x = i;
			B.p3.y = z_func( i, j + Y_STEP_SIZE);
			B.p3.z = j + Y_STEP_SIZE;

			B.p2.x = i + X_STEP_SIZE;
			B.p2.y = z_func( i + X_STEP_SIZE, j + Y_STEP_SIZE );
			B.p2.z = j + Y_STEP_SIZE;

			printf ("triangle {\n");
			printf ("\t<%4.4f, %4.4f, %4.4f>,", B.p1.x, B.p1.y, B.p1.z);
			printf ("<%4.4f, %4.4f, %4.4f>,", B.p2.x, B.p2.y, B.p2.z);
			printf ("<%4.4f, %4.4f, %4.4f>\n", B.p3.x, B.p3.y, B.p3.z);
			printf ("}\n");
		}
	}

	printf ("}\n");  /* Close the mesh */
}

float z_func (float x, float y){
/*		return sin(x) * cos(y); */
		return exp(-2*(pow(x,2) + pow(y,2)));
}
