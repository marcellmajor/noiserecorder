set datafile separator ','
set xdata time
set timefmt "%Y-%m-%d_%H-%M-%S"
set key autotitle columnhead
set format x "%H:%M:%S"
set xlabel 'Time'
set ylabel 'Max. volume'
set xtics rotate
plot filename using 1:2 with lines
