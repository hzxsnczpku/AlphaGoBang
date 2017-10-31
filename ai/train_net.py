# @Author: chenyu
# @Date:   20_Oct_2017
# @Email:  yu.chen@pku.edu.cn
# @Filename: mcts.py
# @Last modified by:   chenyu
# @Last modified time: 20_Oct_2017
import os
import sys
used_gpu = sys.argv[1]
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = used_gpu

import tensorflow as tf
import numpy as np
import config

from ai.net import model_fn
from env.gobang import show_np, axis, int2array


def get_data(data_file_name):
    f = open(data_file_name).readlines()
    duplicate = {}
    features = []
    labels = []
    values = []
    for line in f:
        if len(line) < 3:
            continue
        line = [int(i) for i in line.strip('\n').split(',')]
        if len(line) != 4:
            continue
        if abs(line[-1]) > 2:
            continue
        if abs(line[-1]) == 2:
            line[-1] = line[-1] / 2
        if (line[0], line[1], line[3]) in duplicate:
            # many state duplicated
            continue
        duplicate[(line[0], line[1], line[3])] = 0
        example = int2array(line[0:2])
        features.append(example)
        labels.append(line[2])
        values.append(line[3])
    return features, labels, values


def my_numpy_input_fn(x,
                      y,
                      batch_size=128,
                      num_epochs=1,
                      shuffle=True,
                      queue_capacity=2000,
                      num_threads=1):
    """A numpy_input_fn for multi_head estimator.
        x: {'key': numpy arrray}
        y: {'head1': numpy array, 'head2': numpy array, ...}

    """
    import collections
    from tensorflow.python.estimator.inputs.queues import feeding_functions

    def input_fn():
        ordered_dict_x = collections.OrderedDict(
            sorted(x.items(), key=lambda t: t[0]))
        target_keys = []
        for tar_key in y:
            target_keys.append(tar_key)
            ordered_dict_x[tar_key] = y[tar_key]
        queue = feeding_functions._enqueue_data(  # pylint: disable=protected-access
            ordered_dict_x,
            queue_capacity,
            shuffle=shuffle,
            num_threads=num_threads,
            enqueue_size=batch_size,
            num_epochs=num_epochs)
        features = (queue.dequeue_many(batch_size)
                    if num_epochs is None else queue.dequeue_up_to(batch_size))

        if features:
            features.pop(0)
        features = dict(zip(ordered_dict_x.keys(), features))
        target = {}
        for tar_key in target_keys:
            target[tar_key] = features.pop(tar_key)
        return features, target

    return input_fn


def load_data():
    data_file_name = '/data/gobang/warmup'
    features, labels, values = get_data(data_file_name)
    train_size = int(len(features) * 0.7)
    afeatures = np.array(features[:train_size])
    alabels1 = np.array(labels[:train_size])
    alabels2 = np.array(values[:train_size])
    bfeatures = np.array(features[train_size:])
    blabels1 = np.array(labels[train_size:])
    blabels2 = np.array(values[train_size:])

    return {
        'x': afeatures
    }, {
        'policy': alabels1,
        'value': alabels2
    }, {
        'x': bfeatures
    }, {
        'policy': blabels1,
        'value': blabels2
    }


if __name__ == "__main__":
    train_x, train_y, test_x, test_y = load_data()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.5)
    session_config = tf.ConfigProto(gpu_options=gpu_options)
    config = tf.estimator.RunConfig(session_config=session_config)

    train_input_fn = my_numpy_input_fn(train_x, train_y)
    test_input_fn = my_numpy_input_fn(test_x, test_y)
    params = dict(conv_filters=[24] * 4, learning_rate=0.01)
    classifier = tf.estimator.Estimator(
        model_fn=model_fn,
        params=params,
        model_dir="/data/gobang/models/test_resnet/",
        config=config)

    while True:
        try:
            classifier.train(input_fn=train_input_fn)
            classifier.evaluate(input_fn=test_input_fn)
            features = {'x': tf.placeholder(tf.float32, [None, 15, 15, 2])}
            export_input_fn = tf.estimator.export.build_raw_serving_input_receiver_fn(
                features)
            servable_model_dir = "/data/gobang/init"
            servable_model_path = classifier.export_savedmodel(
                servable_model_dir, export_input_fn)
        except KeyboardInterrupt:
            print("USER interrupt")
            # features = {'x': tf.placeholder(tf.float32, [None, 15, 15, 2])}
            # export_input_fn = tf.estimator.export.build_raw_serving_input_receiver_fn(
            #     features)
            # servable_model_dir = "/data/gobang/init"
            # servable_model_path = classifier.export_savedmodel(
            #     servable_model_dir, export_input_fn)
            break
