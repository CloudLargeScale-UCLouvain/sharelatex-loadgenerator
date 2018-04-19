#!/usr/bin/gnuplot

#usage
#i=1; for j in `head -1 cloud.30mins.10users-5321`; do echo $i "${j//\\/}"; ((i++)); done;
# gnuplot -e "m=3" overhead.gp

if (!exists("df1")) df1='../out/dir.core.1800secs.10users-84a9'
if (!exists("df2")) df2='../out/redir.core.1800secs.10users-6e25'
if (!exists("m")) m=2

set xlabel "ms"
set ylabel '%'


#set xrange [0:100]


#set key autotitle columnhead


firstrow = system('head -1 '.df1)
tl = word(firstrow, m)
set title tl

plot df1 using m:1 title "core direct" with lines lw 1.3  lc rgb "red" ,\
	 df2 using m:1 title "core redirect" with lines lw 1.3  lc rgb "brown"
	 
pause mouse close