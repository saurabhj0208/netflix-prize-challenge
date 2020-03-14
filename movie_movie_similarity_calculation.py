from scipy import sparse
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import os
from rmse_calculator import calculate_rmse
import numpy as np
from whoratedwhat import find_if_rated

system_flag = 1

DATA_PATH = 'C:/Users/amedge/Downloads/netflix-prize-data/{}' if system_flag == 1 else \
    'C:/Users/Akshay Medge/Downloads/netflix-prize-data/{}'
FILE_PATH = 'C:/Users/amedge/Desktop/Project/netflix-prize-test/combined_data.csv' if system_flag == 1 else \
    'C:/Users/Akshay Medge/Desktop/Github/ALDA/netflix-prize-test/combined_data.csv'


def predict(user_id, movies_list, movie_user_dictionary, similarity_list, ideal_k=30):
    # logs_file = open("Prediction_logs.txt", "w")
    # logs_file.write("User: {}\n".format(user_id))
    neighbor_count, similarity_rating_sum, similarity_sum = 0, 0, 0
    for movie in movies_list:
        if movie != 0:
            # print("User is of type: {}".format(type(user_id)))
            # logs_file.write("Movie: {}\n".format(movie))
            # logs_file.write("Users who have rated the movie: {}\n".format(list(movie_user_dictionary[movie].keys())))
            if neighbor_count < ideal_k and int(user_id) in list(movie_user_dictionary[movie].keys()):
                neighbor_count += 1
                mov_idx = np.where(movies_list == movie)
                movie_similarity = similarity_list[int(mov_idx[0])]  # movies_list.index(movie)]
                # print("M_sim: {}".format(movie_similarity))
                # print("MUD: {}".format(movie_user_dictionary[movie]))
                similarity_rating_sum += (movie_user_dictionary[movie][int(user_id)] * movie_similarity)
                # print("Sim_Rating_sum: {}".format(similarity_rating_sum))
                similarity_sum += movie_similarity
    # logs_file.close()
    return similarity_rating_sum / similarity_sum


def predict_rating_for(user, similar_movies, m_u_dictionary):
    sorted_similarities = sorted(similar_movies, reverse=True)
    sorted_similar_movie_ids = similar_movies.argsort()[::-1][1:]

    # print("Similarities in a sorted order: {}".format(sorted_similarities))
    # print("Similar Movies in sorted order: {}".format(sorted_similar_movie_ids))

    return predict(user, sorted_similar_movie_ids, m_u_dictionary, sorted_similarities)


def movie_user_rating_mapping(list_file):
    ratings_tmp = {}
    print("Starting to compute Movie --> Users:Rating Mappings...")
    mov_r = {}
    for file in list_file:
        start_file_read = datetime.now()
        with open(DATA_PATH.format(file)) as test:
            for data_line in test:
                if data_line[-2] == ":":
                    j = int(data_line[0:len(data_line) - 2])
                    ratings_tmp = {}
                else:
                    ratings_tmp.update({int(data_line.split(",")[0]): int(data_line.split(",")[1])})
                    mov_r.update({j: ratings_tmp})
        end_file_read = datetime.now()
        print('Done with {} file in {}'.format(file, (end_file_read - start_file_read)))
    print("Mappings computed.\n")
    return mov_r


def similarity_mapping(param):
    similarity_dictionary = {}
    for movie_idx in range(0, len(param)):
        similarity_dictionary[movie_idx] = param[movie_idx]
    print("Similarity Mapping Dictionary: {}".format(similarity_dictionary))
    return similarity_mapping()


print("\n")
program_time_start = datetime.now()
if not os.path.isfile("all_data_sparse_matrix.npz"):
    print("Loading all data....")
    start_load = datetime.now()
    combined_data_df = pd.read_csv(FILE_PATH, names=[
        'movie', 'user', 'rating', 'date'], sep=",")
    end_load = datetime.now()
    print("Loading complete in: {}\n".format(end_load - start_load))

    print("Creating Sparse Matrix....")
    start_sparse = datetime.now()
    training_sparse_matrix = sparse.csr_matrix((combined_data_df.rating.values, (combined_data_df.user.values,
                                                                                 combined_data_df.movie.values)), )
    end_sparse = datetime.now()
    print("Created sparse matrix in time: {}, The shape is: {}".format((end_sparse - start_sparse),
                                                                       training_sparse_matrix.shape))
    sparse.save_npz("all_data_sparse_matrix.npz", training_sparse_matrix)
    print("Saved Sparse Matrix!")
if not os.path.isfile("movie_movie_similarity.npz"):
    print("Loading sparse matrix...")
    training_sparse_matrix = sparse.load_npz("all_data_sparse_matrix.npz")
    start_sim_calc = datetime.now()
    movie_movie_similarity = cosine_similarity(X=training_sparse_matrix.T, dense_output=False)
    end_sim_calc = datetime.now()

    sparse.save_npz("movie_movie_similarity.npz", movie_movie_similarity)
    print("Saved Movie Movie Similarity Matrix on the disk. Calculation Finished in: {}".format(
        end_sim_calc - start_sim_calc))

print("Loading Similarity Matrix...")
m_m_sim_matrix = sparse.load_npz("movie_movie_similarity.npz")
print("Movie Movie similarity matrix has a shape: {}\n".format(m_m_sim_matrix.shape))

start_dict_creation = datetime.now()
movie_users_dictionary = movie_user_rating_mapping(['combined_data_1.txt', 'combined_data_2.txt', 'combined_data_3.txt',
                                                    'combined_data_4.txt'])
end_dict_creation = datetime.now()
print("Time for creating entire dictionary: {}\n".format(end_dict_creation - start_dict_creation))

# Working on actual test data:
print("Prediction for qualifying.txt in progress...")
qualifying_prediction_start = datetime.now()
with open(DATA_PATH.format('qualifying.txt')) as test_data:
    output_file = open("Qualifying_Predictions.txt", "w")
    movie_id = 0
    for test_line in test_data:
        if ":" in test_line:
            movie_id = test_line.strip().replace(":", "")
            output_file.write("For Movie: {}".format(movie_id))
        else:
            user = test_line.split(',')[0]
            prediction = predict_rating_for(user, m_m_sim_matrix[movie_id].toarray().ravel(),
                                            movie_users_dictionary)
            print("Rating for the above movie by User: {} is: {}".format(user, prediction))
            output_file.write("{}:{}".format(test_line.split(',')[0], prediction))
    output_file.close()
qualifying_prediction_end = datetime.now()
print("Prediction for qualifying.txt completed. Time taken: {}\n".format(qualifying_prediction_end -
                                                                         qualifying_prediction_start))

# Working on Probe data:
test_lines = '200K'
probe_actual_output = []
print("Prediction for probe.txt in progress...")
probe_prediction_start = datetime.now()
with open(DATA_PATH.format('probe_{}.txt').format(test_lines)) as test_data:
    output_file = open("Probe_Predictions.txt", "w")
    movie_id = 0
    for probe_line in test_data:
        if ":" in probe_line:
            movie_id = probe_line.strip().replace(":", "")
            # output_file.write("For Movie: {}".format(movie_id))
            print("Predicting for Movie: {}".format(movie_id))
        else:
            # Actual Value for RMSE
            user = probe_line.split(',')[0]
            probe_actual_output.append(movie_users_dictionary[int(movie_id)][int(user)])
            # For Prediction
            prediction = predict_rating_for(user, m_m_sim_matrix[movie_id].toarray().ravel(),
                                            movie_users_dictionary)
            # print("Rating for the above movie in Probe by User: {} is: {}".format(user, prediction))
            output_file.write("{}\n".format(str(round(prediction))))
    output_file.close()
probe_prediction_end = datetime.now()
print("Prediction for probe.txt completed. Time taken: {}\n".format(probe_prediction_end -
                                                                    probe_prediction_start))

print("I really hope this prints out. If it does, RMSE will be: {}\n".format(calculate_rmse(probe_actual_output)))

# Working on Who rated What:

find_if_rated(m_m_sim_matrix, movie_users_dictionary, 40, 60)

program_time_end = datetime.now()

print("Congratulations Son. Program completed in {}".format(program_time_end - program_time_start))
