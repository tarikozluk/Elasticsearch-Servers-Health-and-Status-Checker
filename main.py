from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from re import search
#todo: Connection String for all elasticsearch cluster in our responsiblity

load_dotenv()
try:
    indexer_es = Elasticsearch([os.getenv("ELASTIC_URL_1")], basic_auth=(os.getenv("ELASTIC_USER_1"), os.getenv("ELASTIC_PASSWORD_1")), verify_certs=False)

    for i in range(1, 13):
        elastic_url = os.getenv("ELASTIC_URL_{}".format(i))
        elastic_user = os.getenv("ELASTIC_USER_{}".format(i))
        elastic_pass = os.getenv("ELASTIC_PASSWORD_{}".format(i))



        try:
            print("Connecting to {}".format(elastic_url))
            es = Elasticsearch([elastic_url], basic_auth=(elastic_user, elastic_pass),verify_certs=False)

            cluster_name= es.info()['cluster_name']
            elastic_version= es.info()['version']['number']

            elastic_health= es.cluster.health()['status']
            number_of_nodes= es.cluster.health()['number_of_nodes']
            number_of_data_nodes= es.cluster.health()['number_of_data_nodes']
            active_primary_shards= es.cluster.health()['active_primary_shards']
            active_shards= es.cluster.health()['active_shards']
            relocating_shards= es.cluster.health()['relocating_shards']
            initializing_shards= es.cluster.health()['initializing_shards']
            unassigned_shards= es.cluster.health()['unassigned_shards']
            delayed_unassigned_shards= es.cluster.health()['delayed_unassigned_shards']
            number_of_pending_tasks= es.cluster.health()['number_of_pending_tasks']
            number_of_in_flight_fetch= es.cluster.health()['number_of_in_flight_fetch']
            task_max_waiting_in_queue_millis= es.cluster.health()['task_max_waiting_in_queue_millis']
            active_shards_percent_as_number= es.cluster.health()['active_shards_percent_as_number']

            print(es.cat.nodes())
        except:
            print("Something went wrong at {}, when trying to connect".format(elastic_url))

        #todo: indices will be formatted to reach them in Grafana
        indexer_es.index(index=("metricshealth-{}-monitoring_{}".format(cluster_name,datetime.now().strftime("%Y.%m.%d"))).lower(),

                     document={
                           "timestamp": datetime.now(timezone.utc).isoformat(),
                           "cluster_name": cluster_name,
                           "elastic_version": elastic_version,
                           "elastic_health": elastic_health,
                           "number_of_nodes": number_of_nodes,
                           "number_of_data_nodes": number_of_data_nodes,
                           "active_primary_shards": active_primary_shards,
                           "active_shards": active_shards,
                           "relocating_shards": relocating_shards,
                           "initializing_shards": initializing_shards,
                           "unassigned_shards": unassigned_shards,
                           "delayed_unassigned_shards": delayed_unassigned_shards,
                           "number_of_pending_tasks": number_of_pending_tasks,
                           "number_of_in_flight_fetch": number_of_in_flight_fetch,
                           "task_max_waiting_in_queue_millis": task_max_waiting_in_queue_millis,
                           "active_shards_percent_as_number": active_shards_percent_as_number
                           #"Nodes": es.cat.nodes(),
                           })

except Exception as e:
    print("Something went wrong: {}".format(e))





