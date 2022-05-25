#!/bin/bash

#  $1 represents the name of the Micro to map
#  $2 represents the user to which the Micro should be mapped

created=0
grep -q $2 /etc/passwd
if [ $? -eq 0  ]; then
       home=$( getent passwd $2 | cut -d: -f6 )
       
	   if [ ! -d $home/data ]; then
              mkdir $home/data
              chown -R $2:users $home/data
              chmod -R 770 $home/data            
       fi
       
       if [ ! -d /home/bio/$1/$2 ]; then
              mkdir /home/bio/$1/$2
              chown -R $2:users /home/bio/$1/$2    
              created=1
       fi

       cd "$home/data"
       if [ ! -h $1 ]; then
              target="/home/bio/$1/$2"
              ln -sT $target $1
              chown -R $2:users $1
              created=1
       fi        

fi

if [ $created -eq 0  ]; then
     echo "Done nothing."
     exit 1
else echo -e "\nMicro $1 was created successfully! "
fi
