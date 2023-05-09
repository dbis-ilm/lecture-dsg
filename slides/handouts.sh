#!/bin/sh
PARAMS='--a4paper --landscape'
pdfjam $PARAMS --outfile handouts/dsg-1.pdf main.pdf 1-30
pdfjam $PARAMS --outfile handouts/dsg-2.pdf main.pdf 31-72
pdfjam $PARAMS --outfile handouts/dsg-3.pdf main.pdf 73-137
pdfjam $PARAMS --outfile handouts/dsg-4.pdf main.pdf 142-212
#pdfjam $PARAMS --outfile handouts/ds-4.pdf main.pdf 272-467
#pdfjam $PARAMS --outfile handouts/ds-5.pdf main.pdf 468-552
#pdfjam $PARAMS --outfile handouts/ds-6.pdf main.pdf 553-648
#pdfjam $PARAMS --outfile handouts/ds-7.pdf main.pdf 655-710
