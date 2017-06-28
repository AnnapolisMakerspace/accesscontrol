
export user_data_dir="/home/pi/source/user_data"
cd $user_data_dir

${user_data_dir}/get_contacts.sh '<---redacted--->' | \
	${user_data_dir}/parse_contact_data.sh > \
					${user_data_dir}/ams_user_data.tmp

if ! cmp ams_user_data ams_user_data.tmp;
then
	echo "files differ, updates have been made to wildapricot users..."
	mv ${user_data_dir}/ams_user_data.tmp ${user_data_dir}/ams_user_data
	chown pi:pi ${user_data_dir}/ams_user_data
	sudo systemctl restart system_controller.service
fi

rm ${user_data_dir}/ams_user_data.tmp
	
