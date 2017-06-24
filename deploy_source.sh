

source_root=${2:-"source"}
syscon_host=${2:-"zerow"}
remote_root=${3:-"/home/pi/"}


source_tarball=${source_root}.tgz
echo "tarball name: ${source_tarball}"


tar -zcvf $source_tarball ${source_root}/*

scp $source_tarball ${syscon_host}:/${remote_root}

ssh $syscon_host -C "cd ${remote_root} ; \
    tar -xzvf ${source_tarball} ; \
    rm ${source_tarball}"

# ssh $syscon_host -C "cd ${remote_root} ; \
#     tar -xzvf ${source_tarball} ; \
#     rm ${source_tarball}"
