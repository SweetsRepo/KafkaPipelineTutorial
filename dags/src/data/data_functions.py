from ensurepip import bootstrap
from kafka import KafkaConsumer
from json import loads
import numpy as np
import time, pickle, os, logging

def decode_json(jsons_comb):
    x_train = loads(jsons_comb[0])
    y_train = loads(jsons_comb[1])
    return x_train, y_train

def get_data_from_kafka(**kwargs):
    # break connection if consumer locks for > 3s, automatically set to earliest offset, offsets are commited automatically by consumer
    consumer = KafkaConsumer(
        kwargs["topic"],
        bootstrap_servers = [kwargs["client"]],
        consumer_timeout_ms = 3000,
        auto_offset_reset = "earliest",
        enable_auto_commit = True,
        value_deserializer = lambda x : loads(x.decode("utf-8"))
    )
    try:
        xs = []
        yx = []

        for message in consumer:
            message = message.value
            x, y = decode_json(message)

            xs.append(x)
            ys.append(y)

        xs = np.array(xs).reshape(-1, 28, 28, 1)            # put Xs in the right shape for our CNN
        ys = np.array(ys).reshape(-1)                       # put ys in the right shape for our CNN

        new_samples = [xs, ys]

        pickle.dump(new_samples, open(os.getcwd()+kwargs['path_new_data']+str(time.strftime("%Y%m%d_%H%M"))+"_new_samples.p", "wb"))     # write data

        logging.info(str(xs.shape[0])+' new samples retrieved')

        consumer.close()

    except Exception as e:
        print(e)
        logging.info('Error: '+e)


def load_data(**kwargs):

    # Load the Kafka-fetched data that is stored in the to_use_for_model_update folder

    for file_d in os.listdir(os.getcwd()+kwargs['path_new_data']):

        if 'new_samples.p' in file_d:

            new_samples = pickle.load(open(os.getcwd()+kwargs['path_new_data'] + file_d, "rb"))
            test_set = pickle.load(open(os.getcwd()+kwargs['path_test_set'], "rb"))

            logging.info('data loaded')

            return [new_samples, test_set]

        else:
            logging.info('no data found')
