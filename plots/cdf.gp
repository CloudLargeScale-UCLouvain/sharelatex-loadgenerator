#!/usr/bin/gnuplot


if (!exists("df1")) df1='../out/cloud.30mins.10users-5321'
if (!exists("df2")) df2='../out/edge.30mins.10users-c9fe'
if (!exists("m")) m=2

set xlabel "ms"
set ylabel '%'


#set key autotitle columnhead


firstrow = system('head -1 '.df1)
tl = word(firstrow, m)
set title tl

plot df1 using m:1 title "cloud" with lines lw 1.3  lc rgb "red" ,\
	 df2 using m:1 title "edge" with lines lw 1.3  lc rgb "blue" 
	 
pause mouse close