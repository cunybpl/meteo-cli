# meteo-cli 

This is a simple helper cli to help managea meteo station, isd and normalized data needed specifically for bema deployments. 

Unlike the previous bulk loader that was built directly into `bemadb` this cli simply works only with csv input and output and is more in Unix style. 

It will munge the dataframe output directly into a format suitable for bulk upload into a bema deployment. The scripts folder contains the neccesary steps to achieve this in a data pipeline using `psql`.


## commands
 
`$ meteo-cli --help` will bring up the documentation. 

