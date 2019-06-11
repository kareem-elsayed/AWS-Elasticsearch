import json
import requests
import re


def get_elastic_indices():
    elastic_url = input('Select Elasticsearch Num : '
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
    es_req = requests.get(es_url + "/_cat/indices?h=index")
    logstash_reg = re.compile(r'logstash-\d\d\d\d.\d\d.\d\d')
    new_data = logstash_reg.findall(es_req.text)
    sorted_data = sorted(new_data)
    print(sorted_data)
    while True:
        insert_indices = input("Select indices [Press any key to exit]: ")
        if not insert_indices.startswith('logstash'):
            print("Done")
            exit()
        delete_indices = es_url + '/' + insert_indices
        requests.delete(delete_indices)
        print('Deleted....')


list_and_del()
