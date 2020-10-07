import argparse
import json
import numpy as np
import pandas as pd
np.random.seed(1)


def series_to_obj(ts, cat=None):
    """This functions convert pandas.Series objects 
    into the appropriate JSON strings that DeepAR can consume.
    """
    obj = {"start": str(ts.index[0]), "target": list(ts)}
    if cat is not None:
        obj["cat"] = cat
    return obj

def series_to_jsonline(ts, cat=None):
    return json.dumps(series_to_obj(ts, cat))

def write_data_to_file(path, data):
    with open(path, 'wb') as fp:
        for ts in time_series_training:
            fp.write(series_to_jsonline(ts).encode('utf-8'))
            fp.write('\n'.encode('utf-8'))
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str)
    args, _ = parser.parse_known_args()
    
    freq = 'H'
    prediction_length = 48
    t0 = '2016-01-01 00:00:00'
    data_length = 400
    num_ts = 200
    period = 24
    
    print('GENERATING DATASET')
    time_series = []
    for k in range(num_ts):
        level = 10 * np.random.rand()
        seas_amplitude = (0.1 + 0.3*np.random.rand()) * level
        sig = 0.05 * level # noise parameter (constant in time)
        time_ticks = np.array(range(data_length))
        source = level + seas_amplitude*np.sin(time_ticks*(2*np.pi)/period)
        noise = sig*np.random.randn(data_length)
        data = source + noise
        index = pd.date_range(start=t0, freq=freq, periods=data_length)
        time_series.append(pd.Series(data=data, index=index))

    time_series_training = []
    for ts in time_series:
        time_series_training.append(ts[:-prediction_length])        

    print('SAVING DATASETS INTO OUTPUT FOLDER')
    write_data_to_file(f'{args.output}/train.json', time_series_training)
    write_data_to_file(f'{args.output}/test.json', time_series)