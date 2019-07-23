#include <stdio.h>
#include <stdlib.h>

void main(){

	system("./linux-4.14/tools/perf/perf stat -a --per-core -e r73,r75 ~/sysbench");

}
