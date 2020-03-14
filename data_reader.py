from datetime import datetime
import os

start_total = datetime.now()
if not os.path.isfile('combined_data.csv'):
    data = open('combined_data.csv', 'w')

    files_to_be_read = ['combined_data_1.txt', 'combined_data_2.txt', 'combined_data_3.txt', 'combined_data_4.txt']

    for file in files_to_be_read:
        start_individual = datetime.now()
        with open('C:/Users/Akshay Medge/Downloads/netflix-prize-data/{}'.format(file)) as opened_file:
            for line in opened_file:
                line = line.strip()
                if line.endswith(':'):
                    m_id = line.replace(':', '')
                else:
                    row = [x for x in line.split(',')]    # row = line.split(',')
                    row.insert(0, m_id)
                    data.write(','.join(row))   # data.write(','+'row')
                    data.write('\n')
            end_individual = datetime.now()
            print('done with {} file in {}'.format(file, (end_individual - start_individual)))
    data.close()
end_total = datetime.now()
print("Total Time = {}".format(end_total - start_total))
