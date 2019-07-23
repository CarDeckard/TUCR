#include <stdio.h>

void main(){
	double f = .999;

	for(int k = 0; k < 100; k++){
	for(int j = 0; j < 1000; j++){
	for(int i = 0; i < 1000; i++){
		f *= 1.1;
	}
	for(int i = 0; i < 1000; i++){
		f *= .9;
	}
	}}
	
	printf("%lg\n",f);
}
