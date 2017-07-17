
from math import ceil, sqrt
import time

import pandas as pd
import matplotlib.pyplot as plt


def run_benchmark(short_dataset, medium_dataset, long_dataset,
                  data_size, sim_measure, tokenizer = None, num_repeat = 1, 
                  random_seed = 0, output_file = None):

    # read data
    short_strings = pd.read_csv(short_dataset)
    medium_strings = pd.read_csv(medium_dataset)                                  
    long_strings = pd.read_csv(long_dataset)                                  

    short_len = len(short_strings)
    medium_len = len(medium_strings)
    long_len = len(long_strings)

    # compute individual table size
    table_size = ceil(sqrt(data_size))
    print(table_size)
    # sample strings    
    short_table = list(short_strings.sample(table_size, replace = True, 
                                            random_state = random_seed).values)
    medium_table = list(medium_strings.sample(table_size, replace = True, 
                                              random_state = random_seed).values)
    long_table = list(long_strings.sample(table_size, replace = True, 
                                          random_state = random_seed).values)
    
    tables = [('short', short_table), ('medium', medium_table), 
              ('long', long_table)]

    # run benchmark for each configuration
    bench_output = []
    for i in range(len(tables)):
        for j in range(len(tables)):
            runtimes = profile_runtime(tables[i][1], tables[j][1], tokenizer, 
                                       sim_measure, num_repeat)
            runtimes.append(sum(runtimes)/float(num_repeat))
            runtimes.insert(0, '_'.join([tables[i][0], tables[j][0]]))
            bench_output.append(runtimes)

    header = ['run_'+str(i+1)+' (in secs)' for i in range(num_repeat)]
    header.append('average (in secs)')
    header.insert(0, 'configuration')
    output_table = pd.DataFrame(bench_output, columns = header)

    if output_file:
        pd.to_csv(output_file, index = False)

    return output_table

 
def profile_runtime(table_A, table_B, tokenizer, sim_measure, num_repeat):
    # run benchmark for one configuration
    runtimes = []
    for i in range(num_repeat):
        start_time = time.time()
        for string1 in table_A:
            for string2 in table_B:
                if tokenizer:
                    score = sim_measure(tokenizer(string1[0]), tokenizer(string2[0]))
                else:
                    score = sim_measure(string1[0], string2[0])
        end_time = time.time()
        runtimes.append(end_time-start_time)
    return runtimes


def plot_benchmark(bench_output, output_file, 
                   conf_attr = 'configuration', time_attr = 'average (in secs)'):
    # Generate plot from benchmark output
    plt.plot(bench_output[conf_attr], bench_output[time_attr], marker='o')
    plt.xlabel('Configuration')
    plt.ylabel('Average time (in secs)')
    plt.title('Benchmark plot')
    plt.savefig(output_file)
    print('Plot generated successfully.')
     
