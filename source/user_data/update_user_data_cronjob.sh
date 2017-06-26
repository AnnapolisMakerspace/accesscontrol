
export user_data_dir="/home/pi/source/user_data"
cd $user_data_dir

${user_data_dir}/get_contacts.sh '<---Redacted--->' | \
	${user_data_dir}/parse_contact_data.sh > \
					${user_data_dir}/ams_user_data.tmp

#differ=$(cmp ${user_data_dir}/ams_user_data{,.tmp})

if ! cmp ams_user_data ams_user_data.tmp;
then
	echo "differ!"
	mv ${user_data_dir}/ams_user_data.tmp ${user_data_dir}/ams_user_data
	chown pi:pi ${user_data_dir}/ams_user_data
fi

rm ${user_data_dir}/ams_user_data.tmp
	
