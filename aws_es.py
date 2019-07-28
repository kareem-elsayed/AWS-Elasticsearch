import json
import requests
import re

# load ElasticSearch URLs form config files or you can insert directly ElasticSearch url


def get_elastic_indices():
    elastic_url = input('Select[Number] : '
                        '\n'
                        '[1] Dev'
                        '\n'
                        '[2] Stage'
                        '\n'
                        '[3] Insert your Elasticsearch url'
                        '\n'
                        '> '
                        )
    with open('config.json') as config_file:
        data = json.load(config_file)
        dev_url = data['dev_url']
        stage_url = data['stage_url']
        if elastic_url == '1':
            return dev_url
        elif elastic_url == '2':
            return stage_url
        elif elastic_url == '3':
            elastic_url = input('Insert your Elasticsearch url : ')
        if not elastic_url.endswith('/'):
            return elastic_url + '/'
        else:
            return elastic_url

# Filtering ElasticSearch indices,list Logstash indices


def list_indices():
    global es_url
    es_url = get_elastic_indices()
    es_req = requests.get(es_url + '_cat/indices?h=index')
    logstash_reg = re.compile(r'logstash.*')  # Regex pattern for logstash
    new_data = logstash_reg.findall(es_req.text)
    sorted_data = sorted(new_data)
    results = '\n'.join(sorted_data)
    print(results)
    items = int(input('select range of indices: '))
    for i in sorted_data[:items]:
        print(es_url + i)
        delete_indices = es_url + i
        requests.delete(delete_indices)
        print('Deleted...')




# Select which indices do you want to delete


# def del_indices():
#     while True:
#         insert_indices = input('Select indices [Press any key to exit]: ')
#         if not insert_indices.startswith('logstash'):
#             print('Done')
#             exit()
#         delete_indices = es_url + insert_indices
#         requests.delete(delete_indices)
#         print('Deleted....')


def main():
    list_indices()
    #del_indices()


if __name__ == '__main__':
    main()
