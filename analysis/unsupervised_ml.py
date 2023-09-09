import pandas as pd
import numpy as np
from scipy.stats import chi2
from sklearn.mixture import GaussianMixture
from sklearn.svm import OneClassSVM
from scipy.stats import norm
from sklearn.decomposition import PCA


class UnsupervisedML:

    def __init__(self, df):
        self.df = df
        last_row = self.df.iloc[-1].squeeze()

        self.one_class_SVM(last_row)
        self.PCA(last_row)
        self.mahalanobis_dist(last_row)
        self.GMM(last_row)

    def select_best_model(self, training_trials, training_outputs):
        SVM_entries = []
        PCA_entries = []
        maha_entries = []
        GMM = []

        for row in training_trials:
            SVM_entries.append(self.one_class_SVM(row))
            PCA_entries.append(self.PCA(row))
            maha_entries.append(self.mahalanobis_dist(row))
            GMM.append(self.GMM(row))

        SVM_err = self.penalty(SVM_entries, training_outputs)
        PCA_err = self.penalty(PCA_entries, training_outputs)
        maha_err = self.penalty(PCA_entries, training_outputs)
        GMM_err = self.penalty(GMM, training_outputs)

        if SVM_err == min(SVM_err, PCA_err, maha_err, GMM_err):
            return
        elif PCA_err == min(SVM_err, PCA_err, maha_err, GMM_err):
            return
        elif maha_err == min(SVM_err, PCA_err, maha_err, GMM_err):
            return
        else:
            return

    @staticmethod
    def penalty(result, expected):
        return sum([res - exp for res, exp in zip(result, expected)])

    def one_class_SVM(self, vector):
        # Fit a One-Class SVM model
        svm_model = OneClassSVM(nu=0.05)  # Adjust the 'nu' hyperparameter as needed
        svm_model.fit(self.df)

        # Calculate the decision function score for the new data vector
        distance_score = svm_model.decision_function([vector])[0]

        outlier_probability = norm.cdf(distance_score)

        return outlier_probability

        # print(f"Outlier Probability: {outlier_probability}")

    def PCA(self, vector):
        # Fit a PCA model to your data
        n_components = 2  # Adjust the number of principal components as needed
        pca_model = PCA(n_components=n_components)
        pca_model.fit(self.df)

        # Project the new data vector onto the principal components
        new_data_projected = pca_model.transform([vector])

        # Reconstruct the data vector using the principal components
        reconstructed_data = pca_model.inverse_transform(new_data_projected)

        # Calculate the reconstruction error for the new data vector
        reconstruction_error = np.mean(np.square(vector - reconstructed_data))

        # Convert the reconstruction error to an outlier probability
        # You can adjust this conversion based on your data distribution and needs
        outlier_probability = 1.0 - np.exp(-reconstruction_error)

        return outlier_probability

        # print(f"Outlier Probability: {outlier_probability}")

    def mahalanobis_dist(self, vector):
        # Calculate the mean and covariance matrix of the data vectors
        mean_vector = np.mean(self.df, axis=0)
        cov_matrix = np.cov(self.df, rowvar=False)

        # Calculate the Mahalanobis distance for the new data vector
        diff_vector = vector - mean_vector
        mahalanobis_distance = np.sqrt(np.dot(np.dot(diff_vector, np.linalg.inv(cov_matrix)), diff_vector))

        # Degrees of freedom for the chi-squared distribution
        df_chi2 = len(self.df.columns)

        # Convert Mahalanobis distance to an outlier probability
        outlier_probability = 1.0 - chi2.cdf(mahalanobis_distance ** 2, df_chi2)

        return outlier_probability

        # print(f"Outlier Probability: {outlier_probability}")

    def GMM(self, vector):
        gmm = GaussianMixture(n_components=2)  # You can adjust the number of components
        gmm.fit(self.df)

        # Calculate the log probability density for the new data vector
        log_prob = gmm.score_samples([vector])

        # Calculate the outlier probability (normalized percentile rank)
        outlier_probability = len(log_prob[log_prob <= log_prob[0]]) / len(log_prob)

        return outlier_probability

        # print(f"Outlier Probability: {outlier_probability}")
