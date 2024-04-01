\\_ Commands Instruction _//

<- DISCLAIMER ->
1- ALL commands are tested in Window11 Command prompt
2- There are some function that if u enter commands without arguments it'll ask u to put it (like rename, it'll ask u to enter "From name") this part i did not do it
3- Commands usage is listed below
4- I didn't check the timeout of the connection, so if it is timed out... yeah my code probably error

!!!! MUST type in every argument needed (*), or else my code will error !!!!

behind '*' is the argument u MUST type in to use the commands
behind '#' is the OPTIONAL argument to use the commands

open *hostname/ip #port 
(Default port number is 21)

user #username #password
(This one i do the prompt thingy)

rename *filename *newfilename

get *remote_file #local_file_name
(Default local_file_name is your remote_file's name)

put *local_file #remote_file_name
(Default remote_file_name is your local_file's name)

delete *remote_file

cd *directory_name or '..'

ls #directory_name
(Default will list the files on directory you're at)
