from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

import pandas as pd
import seaborn as sns
sns.set_style('whitegrid')
import operator


# Global variable for how many similar users are needed.
SIMILAR_COUNT = 50


def chunker(file_name):
    count = 0
    print("Starting Chunking:")
    final_df = pd.DataFrame()
    dataframe = pd.read_csv(file_name, names=['movie', 'user', 'rating', 'date'], sep=",", chunksize=100000)
    for chunk in dataframe:
        count += 1
        start = datetime.now()
        final_df = final_df.add(chunk.pivot('user', 'movie', 'rating'), fill_value=0)
        end = datetime.now()
        print("Processed Chunk {} in time {}".format(count, (end - start)))
    return dataframe


# Function to read a particular file and transform it to a Dataframe. ( Modify at Will. )
def create_data():
    user_movie_matrix = [[]]
    movie_id = 0
    file = 'test_chunk.txt'
    file_being_read = open("C:/Users/Akshay Medge/Downloads/netflix-prize-data/{}".format(file))
    for line in file_being_read.readlines():
        if ":" in line:
            movie_id = movie_id + 1
            # print("Appending Movie ID: {}".format(movie_id))
        else:
            line_append = line.strip().split(",")
            line_append.append(movie_id)
            # print(line_append)
            user_movie_matrix.append(line_append)
    # print("Ending : {}".format(file))
    file_being_read.close()
    return pd.DataFrame(user_movie_matrix, columns=['user', 'rating', 'date', 'movie'], dtype=int)


# Function to compute the similarity between users.
def similar_users(sparse_matrix_param):
    start = datetime.now()
    temp = 0
    total_users, _ = sparse_matrix_param.shape

    row_ind, col_ind = sparse_matrix_param.nonzero()
    print("Row Indices: {}".format(row_ind))
    rows, cols, data = list(), list(), list()
    for row in row_ind[:SIMILAR_COUNT]:
        temp = temp + 1
        # prev = datetime.now()
        sim = cosine_similarity(sparse_matrix_param.getrow(row), sparse_matrix_param).ravel()
        top_sim_ind = sim.argsort()[-SIMILAR_COUNT:]
        top_sim_val = sim[top_sim_ind]

        rows.extend([row] * SIMILAR_COUNT)
        cols.extend(top_sim_ind)
        data.extend(top_sim_val)

        if temp % 20 == 0:
            print("computing done for {} users [  time elapsed : {}  ]"
                  .format(temp, datetime.now() - start))

    return sparse.csr_matrix((data, (rows, cols)), shape=(total_users, total_users))


# Function to return a dictionary of similar users mapped to a particular user.
def u_u_matrix_to_dictionary(similarity_matrix):
    similarity_dict = {}

    um_rows = similarity_matrix.row
    um_cols = similarity_matrix.col
    um_data = similarity_matrix.data

    # Procedure for converting a coo matrix to a dictionary in the format: user -> {similar_user1 -> similarity1,
    #                                                                              similar_user2 -> similarity2}
    multiplier = 0
    for user in um_rows[::SIMILAR_COUNT]:
        counter = 0
        similarity_dict[user] = {}
        while counter < SIMILAR_COUNT:
            similarity_dict[user][um_cols[(multiplier * SIMILAR_COUNT) + counter]] = um_data[
                (multiplier * SIMILAR_COUNT) + counter]
            counter += 1
        multiplier += 1

    # Maps the similar users to a particular user by sorting them as per their similarities.
    # Final output format: {user_id -> [list of corresponding similar users]}
    for k, v in similarity_dict.items():
        sorted_similar_users = [user[0] for user in sorted(v.items(), key=lambda kv: kv[1], reverse=True)]
        similarity_dict[k] = sorted_similar_users[1:]

    return similarity_dict


def u_m_rating_matrix_to_dictionary(matrix_param):
    mat_coo = matrix_param.tocoo()

    data = {}

    mat_rows = mat_coo.row
    mat_col = mat_coo.col
    mat_data = mat_coo.data

    for idx in range(len(mat_rows)):
        if mat_rows[idx] in data:
            data[mat_rows[idx]][mat_col[idx]] = mat_data[idx]
        else:
            data[mat_rows[idx]] = {mat_col[idx]: mat_data[idx]}
    return data


final_fight = chunker('C:/Users/Akshay Medge/Desktop/Github/ALDA/netflix-prize-test/combined_data.csv')

# TODO: Read data from all training files.
# # user_movie_df = pd.read_csv('C:/Users/Akshay Medge/Downloads/netflix-prize-data/training_chunk_1_2.csv', sep=',',
# #                              names=['user', 'rating', 'date', 'movie'])
#
# # To drop a row that had all 0 values.
# # user_movie_df.drop(user_movie_df.index[0], inplace=True)
#
# user_movie_df = pd.read_csv('data.csv', sep=",", names=['movie', 'user', 'rating', 'date'])
#
# # Sort movies by user for convenience.
# user_movie_df.sort_values(by='user', inplace=True)
#
# # Predict ratings for similar users:
# # Created a sparse matrix.
# # TODO: Save it in the local storage for future ease of use.
#
# print("Sparse Started")
# # Gives a list in the form: (UserId, MovieId) -> Rating
# sparse_matrix = sparse.csr_matrix((user_movie_df.rating.values,
#                                    (user_movie_df.user.values, user_movie_df.movie.values)))
# print("Sparse Done")
#
# data_mat = u_m_rating_matrix_to_dictionary(sparse_matrix)
#
#
# # COO - Co-ordinate Matrix: Easy to read data as it provides a list of all rows, columns, data index wise.
# # Gives a list in the format of (User1, User2) -> Similarity
# print("Finding Similar Users:")
# user_user_matrix = similar_users(sparse_matrix).tocoo()
# print("Found Similar Users")
# # Convert the matrix to a dictionary for ease of use.
# u_u_dictionary = u_u_matrix_to_dictionary(user_user_matrix)
#
#
# # print(u_u_dictionary)
# # print("Saving:")
# # sparse.save_npz("user_user_sparse_matrix.npz", user_user_matrix)
# # similarities = cosine_similarity(sparse_matrix)
# # print(similarities)
