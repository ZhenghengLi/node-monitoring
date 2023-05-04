this_dir=$(dirname ${BASH_SOURCE[0]:-${(%):-%x}})
prefix_dir=$(cd $this_dir > /dev/null ; pwd)

export PATH=$prefix_dir/bin:$prefix_dir/scripts:$PATH
