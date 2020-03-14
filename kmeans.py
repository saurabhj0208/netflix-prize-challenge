import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import sklearn as sk
import pdb
import collections
import os
from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.decomposition import TruncatedSVD

if not os.path.isfile('kmeans_test.csv'):
    data = open('kmeans_test.csv', 'w')

    # files_to_be_read = ['combined_data_1.txt','combined_data_2.txt','combined_data_3.txt','combined_data_4.txt']
    # files_to_be_read = ['combined_data_1.txt']
    files_to_be_read = ['test_chunk.txt']

    for file in files_to_be_read:
        with open('C:/Users/Akshay Medge/Downloads/netflix-prize-data/{}'.format(file)) as opened_file:
            for line in opened_file:
                line = line.strip()
                if line.endswith(':'):
                    m_id = line.replace(':', '')
                else:
                    row = [x for x in line.split(',')]  # row = line.split(',')
                    row.insert(0, m_id)
                    data.write(','.join(row))  # data.write(','+'row')
                    data.write('\n')
            print('done with {} file'.format(file))
    data.close()

# print('I am here')
user_rating_dataframe = pd.read_csv('kmeans_test.csv', sep=",", names=['MovieID', 'UserID', 'Rating', 'Date'])
user_rating_m = user_rating_dataframe[['MovieID', 'UserID', 'Rating']]
# print(user_rating_m.head())

print('reading from disk')
if (os.path.isfile('train_1_sparse_m.npz')):
    train_sparse_m = sparse.load_npz('train_1_sparse_m.npz')
    print("present")
else:
    train_sparse_m = sparse.csr_matrix(
        (user_rating_m.Rating.values, (user_rating_m.UserID.values, user_rating_m.MovieID.values)), )
    sparse.save_npz("train_1_sparse_m.npz", train_sparse_m)
    # sparse.save_npz("train_sparse_matrix.npz",train_sparse_m)

    # train_sparse_matrix = sparse.csr_matrix((train_df.rating.values, (train_df.user.values,train_df.movie.values)), )
    #
    # print('Done. It\'s shape is : (user, movie) : ', train_sparse_matrix.shape)
    # print('Saving it into disk for furthur usage..')
    # # save it into disk
    # sparse.save_npz("train_sparse_matrix.npz", train_sparse_matrix)
    # print('Done..\n')

# train_sparse_m.todense()
# print(train_sparse_m.shape)
# prin(train_sparse_m[0:])
# print(train_sparse_m.shape)


# user_data_rating_frame = pd.read_csv('output_file.csv',sep=',',names=['MovieID','UserID','Rating','Date'])
# #print(user_data_rating_frame)
# user_rating_matrix = user_data_rating_frame.pivot(index = 'UserID',columns='MovieID',values='Rating')
# print(user_rating_matrix)
#
# user_rating_matrix.fillna(0)
# print(user_rating_matrix.head(10))
print('starts here')
within_cluster_sum_square = []

for i in range(1, 21):
    labeler = KMeans(n_clusters=i)
    labeler.fit(train_sparse_m)
    within_cluster_sum_square.append(labeler.inertia_)
    print('done for i= {}'.format(i))

print(within_cluster_sum_square)
plt.plot(range(1, 21), within_cluster_sum_square)
plt.show()

# Read again
# print('starting here')
# user_movie_ratings_df_svd_model = TruncatedSVD(n_components=500, algorithm='randomized', random_state=15)
# user_movie_trunc_matrix = user_movie_ratings_df_svd_model.fit_transform(train_sparse_m)
# if not os.path.isfile('user_movie_trunc_matrix.npz'):
#     user_movie_svd_trunc_matrix = sparse.csr_matrix(user_movie_trunc_matrix)
#     sparse.save_npz('user_movie_trunc_matrix.npz',user_movie_svd_trunc_matrix)
# else:
#     user_movie_svd_trunc_matrix = sparse.load_npz('user_movie_trunc_matrix.npz')
# print(user_movie_trunc_matrix.shape)
