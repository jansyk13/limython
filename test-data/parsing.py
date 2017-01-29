#!/usr/bin/env python

num_lines_half = sum(1 for line in open('raw_data'))/2

with open('raw_data', 'r') as f:
    with open("training_data.sql", "a") as training_data_file:
        with open("test_data.sql", "a") as test_data_file:
            for i,line in enumerate(f):
                values = line.split()
                if len(values) != 7:
                    print(values)
                    continue
                values[1] = values[1].strip("[]")
                values[2] = values[2].strip('"')
                values[4] = values[4].strip('"')
                values[6] = values[6] if values[6] != '-' else 'NULL'
                table = 'training_data' if i <= num_lines_half \
                    else 'test_data'
                insert = "INSERT INTO %s (source, time_stamp, method," + \
                    " url, protocol, status, payload_size) VALUES " + \
                    "(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s); \n"
                    % (table, values[0], values[1], values[2], values[3], \
                     values[4], values[5], value[6])
                if i <= num_lines_half:
                    training_data_file.write(insert)
                else:
                    test_data_file.write(insert)
