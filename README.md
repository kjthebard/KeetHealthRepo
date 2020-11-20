# KeetHealthRepo
##Coding Challenge

Hello! To run the solution to the coding challenge will require some set up. If you are familiar with Docker this should
be a breeze. In this code challenge I used a localhost docker image to host a version of PostgresDB so that I could verify 
my solution. 

##Docker Init
For those who have never used docker before I will walk you through how to set up a postgreSQL docker image. 

To start: please download the latest image of postgreSQL, you can do this by running this command:

docker run -d --name keet-postgres -p 5432:5432 -e POSTGRES_PASSWORD=epona27 -e PGDATA=/var/lib/postgresql/data/pgdata -v /custom/mount:/var/lib/postgresql/data postgres

I also have included this in the repository itself under the docker folder just incase! Remember to expose the port, 
otherwise you will be wondering why your python won't connect

##Database Init
Next, we need to create a database that we can use to load the data to! In my solution I created a database called 
"dev_keet" This is **very important** that the database be named the same. Otherwise the solution will not work! 

## Python main runner 
Once you have created the database you can initialize the solution by using the main.py function. This script utilized
the classes written in the solution folder. This is where the magic happens! There are two classes, one to Load the data
and another to Transform the data. I have commented my work (more on the transformation side) to show my thought process

## Improvements
While the solution I came up with is extremely simple, I have added some additional code on how to turn code like this
over to production. I will explain each idea here:

### Structure for Scale

This was more of a toy dataset, to solve a problem within a limited scope, I made design choices with that in mind.
However, some decisions I made will not work at scale. For example: Using a select * statement, will not work with 
larger datasets, in these cases it would be very important to only select what you need rather the entire dataset. 
For this use case, I really only needed the id's and the dates! 

Using Cursor objects while great for in memory code yields terrible performance at scale! However, this was the route I
took as creating an s3 bucket location for this dataset seemed like overkill! If I were to use a postgres instance in the
cloud. I would make use of External Tables. 

Lastly the compute. Pandas is great! For small datasets.... At scale I would have used either Spark or Dask depending on
what is available! Spark would have made more sense here as the computations and functions are prebuilt there! However,
If I wanted to do more advanced ML or other permutations I would switch to dask in a heartbeat!

### SQL Templating

I also created a sql templating tool for Dev, Tst, and Prod environments. Essentially, what this load.py is doing is 
creating SQL files that are generated from a template. A Data Engineer can then run these scripts manually or through a CI/CD 
pipeline to deploy dml changes to the database. A big problem in data engineering is making sure that database updates 
that are made manually are tracked in version control. This is the purpose of SQL Templating and can be done in a variety of 
ways. 

I actually took a short cut here and hard coded some of the rendering pieces of the code, but given a couple more hours
I could have turned this into an automatic templater based on the templates in the sql_template folder. You can find the
generated ddl for each environment under the sql_template/sql_ddl folder/. There should be 6 templates, 3 for each environment
multiplied by the 2 yml templates defined in the templates folder.

### Processing multiple files

In a real situation I would want to find a solution that would read the entire directory where the data was located. 

 
 

 

