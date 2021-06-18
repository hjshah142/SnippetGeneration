import json
import os
import tensorflow_hub as hub
import numpy as np
# from sklearn.preprocessing import MinMaxScaler
from discreteMarkovChain import markovChain
from lib.argumentative_computation import ArgumentativeComputation


class ArgsRank:

    def __init__(self, d, mc_method, argumentative_score_method):
        script_dir = os.path.dirname(__file__)
        # print(script_dir)
        f = open(os.path.join(script_dir, "../data/ClaimLexicon.txt"))
        self.claim_markers = f.read().split(", ")
        self.argumentative_score_method = argumentative_score_method

        self.discourse_markers = ["for example", "such as", "for instance", "in the case of", "as revealed by",
                                  "illustrated by",
                                  "because", "so", "therefore", "thus", "consequently", "hence", "similarly",
                                  "likewise",
                                  "as with",
                                  "like", "equally", "in the same way", "first", "second ",
                                  "third,", "finally", "next", "meanwhile", "after", "then", "subsequently",
                                  "above all",
                                  "in particular", "especially", "significantly", "indeed", "notably", "but", "however",
                                  "although",
                                  "unless", "except", "apart from", "as long as", "if", "whereas", "instead of",
                                  "alternatively", "otherwise", "unlike", "on the other hand", "conversely"]

        self.d = d  # TODO: Figure out the best value for this param..
        self.mc_method = mc_method
        self.argumentative_score_method = argumentative_score_method
        print("Markov Chain Method", self.mc_method, "Argumentative Score Method", self.argumentative_score_method,
              "d:", self.d)
        # self.scaler = MinMaxScaler()

        # Create graph and finalize (optional but recommended).

        # g = tf.Graph()
        # with g.as_default():
        #   self.text_input = tf.placeholder(dtype=tf.string, shape=[None])
        #   embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")
        #   self.embed_result = embed(self.text_input)
        #   init_op   = tf.group([tf.global_variables_initializer(), tf.tables_initializer()])
        # g.finalize()

        # self.tf_session = tf.Session(graph=g)
        # self.tf_session.run(init_op)
        # tf.config.list_physical_devices('GPU')
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
        self.argumentative_computation = ArgumentativeComputation()

    def power_method(self, M, epsilon):
        """
        Apply power methode to calculate stationary distribution for Matrix M
        :param M: numpy matrix
        :param epsilon:
        :return:
        """
        t = 0
        p_t = (np.ones((M.shape[0], 1)) * (1 / M.shape[0]))
        while True:

            t = t + 1
            p_prev = p_t
            p_t = np.dot(M.T, p_t)

            if np.isnan(p_t).any():
                break

            residual = np.linalg.norm(p_t - p_prev)

            if residual < epsilon:
                break
        return p_t

    def normalize_by_rowsum(self, M):
        for i in range(M.shape[0]):
            sum = np.sum(M[i])
            for j in range(M.shape[1]):
                M[i][j] = M[i][j] / sum
        return M

    def run_and_plot(self, session_, input_tensor_, messages_, encoding_tensor):
        message_embeddings_ = session_.run(
            encoding_tensor, feed_dict={input_tensor_: messages_})
        # plot_similarity(messages_, message_embeddings_, 0)
        return message_embeddings_

    def add_argumentative_score(self, cluster):
        """
        Create numpy array with aij = argumentativeness of sentence j
        :param cluster: cluster of arguments
        :return: (numpy array) teleportation matrix
        """
        # print(self.argumentative_score_method)

        row = []
        if self.argumentative_score_method == "argument_score":

            for argument_j in cluster:
                # print(len(argument_j.sentences))
                for idx, sentence_j in enumerate(argument_j.sentences):
                    argumentative_score = self.argumentative_computation.predict_argumentative_score(sentence_j)
                    value = argumentative_score
                    row.append(value)

        if self.argumentative_score_method == "claim_score":
            for argument_j in cluster:
                # print(len(argument_j.sentences))
                for idx, sentence_j in enumerate(argument_j.sentences):
                    claim_score = self.argumentative_computation.predict_claim_probability(sentence_j)
                    value = claim_score
                    row.append(value)

        if self.argumentative_score_method == "hybrid_score":
            for argument_j in cluster:
                # print(len(argument_j.sentences))
                for idx, sentence_j in enumerate(argument_j.sentences):

                    argumentative_score = self.argumentative_computation.predict_argumentative_score(sentence_j)
                    if argumentative_score >= 0.5:
                        claim_score = self.argumentative_computation.predict_claim_probability(sentence_j)
                        value = claim_score * 0.5 + argumentative_score * 0.5
                        row.append(value)
                    else:
                        row.append(argumentative_score)
        if self.argumentative_score_method == "discourse_claim_markers":
            for argument_j in cluster:
                for idx, sentence_j in enumerate(argument_j.sentences):
                    value = 1.0
                    for marker in self.discourse_markers:
                        if marker in sentence_j.lower():
                            value += 1
                    if any(claim_ind in sentence_j.lower() for claim_ind in self.claim_markers):
                        value += 1
                    row.append(value)

        message_embedding = []
        for argument in cluster:
            for sentence in argument.sentences:
                message_embedding.append(row)

        message_embedding = np.array(message_embedding)
        if self.argumentative_score_method == "discourse_claim_markers":
            message_embedding = self.normalize_by_rowsum(message_embedding)
        return np.array(message_embedding)

    def sem_similarty_scoring(self, clusters):
        """
        Run biased PageRank using Universal Sentence Encoder to receive embedding.
        Calls add add_argumentative_score() and add_syn_similarity().
        Computes similarity to conclusion.
        :param clusters:
        :return:
        """

        messages = []
        for idx, cluster in enumerate(clusters):
            messages = []
            for argument in cluster:
                messages = messages + argument.sentences
            # messages = cluster[0].sentences
            # print(len(messages))

            if self.d == 0:
                message_embedding = [message.numpy() for message in self.embed(messages)]
                # self.tf_session.run(self.embed_result, feed_dict={self.text_input: messages})
                sim = np.inner(message_embedding, message_embedding)
                sim_message = self.normalize_by_rowsum(sim)
                M = np.array(sim_message) * (1 - self.d)

            if self.d == 1.0:
                # print("d =1")
                matrix = self.add_argumentative_score(cluster)
                M = np.array(matrix) * self.d

            if 0 < self.d < 1.0:
                message_embedding = [message.numpy() for message in self.embed(messages)]
                # print("d is between 0 to 1")
                # self.tf_session.run(self.embed_result, feed_dict={self.text_input: messages})

                sim = np.inner(message_embedding, message_embedding)
                sim_message = self.normalize_by_rowsum(sim)
                matrix = self.add_argumentative_score(cluster)
                M = np.array(sim_message) * (1 - self.d) + np.array(matrix) * self.d


            # print("M", M)
            # p = self.power_method(M, 0.0000001)
            mc = markovChain(M)
            mc.computePi(method=self.mc_method)
            p = mc.pi
            # print("P", p)
            x = 0
            for i in range(len(cluster)):
                if not cluster[i].score:
                    score_exists = False
                else:
                    score_exists = True
                for j in range(len(cluster[i].sentences)):
                    if score_exists:
                        cluster[i].score[j] += p[x]
                        cluster[i].score[j] = cluster[i].score[j]

                    else:
                        cluster[i].score.append(p[x])
                    x += 1

                if (len(cluster[i].score) > 1):
                    cluster[i].score = list(
                        (cluster[i].score - min(cluster[i].score)) / (
                                max(cluster[i].score) - min(cluster[i].score)))
                else:
                    cluster[i].score = [1]

    def generate_snippet(self, args):

        output = []

        self.sem_similarty_scoring(args)
        for arguments in args:
            arg = arguments[0]
            arg_snippet = {}
            # processing snippet title
            snippet_title = arg.get_topK(1).tolist()[0]
            # snippet_title_span = self.find_span(arg_text, snippet_title)
            arg_snippet['id'] = arg.id
            arg_snippet['snippet-title'] = snippet_title

            # processing snippet body
            snippet_body_sentences = arg.get_topK(2).tolist()
            arg_snippet['snippets-text'] = snippet_body_sentences
            arg_snippet['aspects'] = arg.aspects
            arg_snippet['sentences'] = arg.premises

            output.append(arg_snippet)

        return output


def get_stored_snippets():
    script_dir = os.path.dirname(__file__)
    stored_snippets = json.load(open(os.path.join(script_dir, "../data/snippets.txt")))
    return stored_snippets