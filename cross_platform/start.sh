#!/usr/bin/env bash

export BROKER_CLOUD=172.17.0.1

export BROKER_FOG=172.17.0.1

export HOST_MYSQL=172.17.0.1

export HOST_INFLUXDB=172.17.0.1

export MODE=PULL

export TIME_COLLECT=5

export TIME_UPDATE_CONF=5


#Forwarder Cloud to Fog
docker run -itd --name cloud-to-fog -e "BROKER_CLOUD=$BROKER_CLOUD" -e "BROKER_FOG=$BROKER_FOG" haiquan5396/forwarder_cloud_to_fog:1.2

#Forwarder Fog to Cloud
docker run -dit --name fog-to-cloud -e "BROKER_CLOUD=$BROKER_CLOUD" -e "BROKER_FOG=$BROKER_FOG" haiquan5396/forwarder_fog_to_cloud:1.2-amd

#Filter
docker run -dit --name filter -e "BROKER_FOG=$BROKER_FOG" haiquan5396/filter:1.2-amd

#Registry

docker run -itd --name registry -e "BROKER_CLOUD=$BROKER_CLOUD" -e "HOST_MYSQL=$HOST_MYSQL" -e "MODE=$MODE" haiquan5396/registry:1.2

#Collector

docker run -itd --name collector -e "BROKER_CLOUD=$BROKER_CLOUD" -e "MODE=$MODE" haiquan5396/collector:1.2

#DBCollector

docker run -itd --name db-reader -e "BROKER_CLOUD=$BROKER_CLOUD" -e "HOST_INFLUXDB=$HOST_INFLUXDB" haiquan5396/db-reader:1.2
docker run -itd --name db-write -e "BROKER_CLOUD=$BROKER_CLOUD" -e "HOST_INFLUXDB=$HOST_INFLUXDB" -v /etc/localtime:/etc/localtime:ro haiquan5396/db-writer:1.2




