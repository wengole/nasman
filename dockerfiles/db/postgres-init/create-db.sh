#!/bin/bash
echo "******CREATING DOCKER DATABASE ******"
gosu postgres postgres --single <<- EOSQL
   CREATE ROLE nasman SUPERUSER LOGIN UNENCRYPTED PASSWORD 'nasman' ;
   CREATE DATABASE nasman OWNER nasman;
EOSQL
echo ""
echo "******DOCKER DATABASE CREATED******"
