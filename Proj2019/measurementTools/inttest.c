#include <stdio.h>

void main(){
	long f = 999;

	for(int k = 0; k < 500; k++){
	for(int j = 0; j < 1000; j++){
	for(int i = 0; i < 1000; i++){
		f *= 1100;
	}
	for(int i = 0; i < 1000; i++){
		f /= 900;
	}
	}}
	
	printf("%ld\n",f);
}
