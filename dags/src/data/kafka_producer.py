from ensurepip import bootstrap
from kafka import KafkaProducer
import random, pickle, os, logging
from time import sleep
from json import dumps

def encode_to_json(x_train, y_train):
    x = dumps(x_train.tolist())
    y = dumps(y_train.tolist())
    jsons_comb = [x, y]

    return jsons_comb

def generate_stream(**kwargs):
    producer = KafkaProducer(bootstrap_servers = ["kafka: 9092"],
        value_serializer = lambda x: dumps(x).encode("utf-8")
    )

    # Load the sample array. Col0 is x values, Col1 is y values
    stream_sample = pickle.load(open(os.getcwd() + kwargs["path_stream_sample"], "rb"))
    rand = random.sample(range(0, 20000), 200)

    x_new = stream_sample[0]
    y_new = stream_sample[1]

    for i in rand:
        json_comb = encode_to_json(x_new[i], y_new[i])
        producer.send("TopicA", value=json_comb)
        logging.info("Sent number: {}".format(y_new[i]))
        sleep(1)

    producer.close()
