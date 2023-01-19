 - The main flask app is in query_generation.py.  
 - The templates directory holds query_gen.html, where the html for the page is. 
 - The paragraphs for each topic are held in topic_paragraphs.csv. 
 - Backup.sh backs up the response csv files in a .tar.gz filem saved in the backups directory. This can be run as a cronjob every few hours to back things up.
 - Each session has a CSV attached to it with their responses. These are saved in the query_gen_results directory.

Cronjob:\
The cronjob to backup the files 4 hours can be set up with:\
0 */4 * * * cd query_generation && ./backup.sh\
This is assuming that the files in this folder are in a directory called query_generation