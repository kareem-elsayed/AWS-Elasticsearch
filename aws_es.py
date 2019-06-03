import os
import json


def get_elastic_indices():
    elastic_url: str = input('Select Elasticsearch Num : '
                             '\n'
                             "[1] Dev"
                             '\n'
                             "[2] Stage"
                             '\n'
                             '[3] Insert your Elasticsearch url'
                             '\n'
                             "##################################"
                             '\n'
                             )
    with open('config.json') as config_file:
        data = json.load(config_file)
        dev_url = data['dev_url']
        stage_url = data['stage_url']
        if elastic_url == "1":
            return dev_url
        elif elastic_url == "2":
            return stage_url
        elif elastic_url == "3":
            elastic_url = input("Insert your Elasticsearch url : ")
        if not elastic_url.startswith('https'):
            return "https://" + elastic_url
        else:
            return elastic_url


def list_and_del():
    es_url = get_elastic_indices()
    os.system(f'curl -XGET {es_url}"/_cat/indices?h=index" | grep "logstash-*" > indices.txt')
    with open("indices.txt", "r") as elastic_file:
        elastic_data = elastic_file.readlines()
        all_indices = [remove_new_line.replace('\n', '') for remove_new_line in elastic_data]
        all_indices.sort()
    for indices in all_indices:
        print(indices)
    while True:
        insert_indices = input("Select indices [Press any key to exit]: ")
        if not insert_indices.startswith('logstash'):
            break
        delete_indices = f'curl -XDELETE {es_url}"/"{insert_indices}'
        os.system(delete_indices)
        print('\n')
    print("Done")


list_and_del()
