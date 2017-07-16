
export user_data_dir="/home/pi/source/user_data"
cd $user_data_dir

${user_data_dir}/get_contacts.sh 'redacted' | \
	${user_data_dir}/parse_contact_data.sh > \
					${user_data_dir}/ams_user_data.tmp

if ! cmp ams_user_data ams_user_data.tmp;
then
	echo $(date "+%Y-%m-%d:%H:%M:%S")
	echo "files differ, updates have been made to wildapricot users..."
	mv ${user_data_dir}/ams_user_data.tmp ${user_data_dir}/ams_user_data
	chown pi:pi ${user_data_dir}/ams_user_data
	echo "new user file in place, restarting system_controller service"

	echo "stopping services..."
	sudo systemctl stop ac-system-controller.service
	sudo systemctl stop ac-relay-controller.service	
	sudo systemctl stop ac-scanner.service
	echo "done"
	
	echo "starting services..."
	sudo systemctl start ac-system-controller.service
	sudo systemctl start ac-relay-controller.service	
	sudo systemctl start ac-scanner.service
	echo "done"
	
fi

rm ${user_data_dir}/ams_user_data.tmp
	
