wget https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_01M_2021_4326.geojson
wget https://gisco-services.ec.europa.eu/distribution/v2/nuts/geojson/NUTS_RG_60M_2021_4326.geojson

ogr2ogr -f PostgreSQL PG:"host=localhost port=5432 dbname=hexadmin user=hexadmin password=mypassword" -nln "nuts_rg_60M_2021" NUTS_RG_01M_2021_4326.geojson
ogr2ogr -f PostgreSQL PG:"host=localhost port=5432 dbname=hexadmin user=hexadmin password=mypassword" -nln "nuts_rg_60M_2021" NUTS_RG_60M_2021_4326.geojson

rm NUTS_RG_01M_2021_4326.geojson
rm NUTS_RG_60M_2021_4326.geojson