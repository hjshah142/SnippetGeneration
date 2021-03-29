import json
import os
import tensorflow_hub as hub
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from discreteMarkovChain import markovChain


class ArgsRank:

    def __init__(self):
        script_dir = os.path.dirname(__file__)
        print(script_dir)
        f = open(os.path.join(script_dir, "../data/ClaimLexicon.txt"))
        self.claim_markers = f.read().split(", ")
        # for m in CLAIM_MARKERS:
        # print(len(self.claim_markers))
        # print(m)

        self.discourse_markers = ["for example", "such as", "for instance", "in the case of", "as revealed by",
                                  "illustrated by",
                                  "because", "so", "therefore", "thus", "consequently", "hence", "similariy",
                                  "likewise",
                                  "as with",
                                  "like", "equally", "in the same way", "first", "second ",
                                  "third,", "finally", "next", "meanwhile", "after", "then", "subsequently",
                                  "above all",
                                  "in particular", "especially", "significantly", "indeed", "notably", "but", "however",
                                  "although",
                                  "unless", "except", "apart from", "as long as", "if", "whereas", "instead of",
                                  "alternatively", "otherwise", "unlike", "on the other hand", "conversely"]

        self.d = 1  # TODO: Figure out the best value for this param..
        self.scaler = MinMaxScaler()

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
        self.embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

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

    def add_tp_ratio(self, sentences):
        """
        Create numpy array with aij = argumentativeness of sentence j


        :param sentences: argument premise
        :return: (numpy array) teleportation marix
        """
        # TODO research for other methods
        row = []

        for idx, sentence_j in enumerate(sentences):
            value = 0.00001
            for marker in self.discourse_markers:
                if marker in sentence_j.lower():
                    value += 1
            if any(claim_ind in sentence_j.lower() for claim_ind in self.claim_markers):
                value += 1

            row.append(value)

        message_embedding = []
        print(len(sentences))
        for sentence_j in sentences:
            message_embedding.append(row)

        message_embedding = np.array(message_embedding)
        message_embedding = self.normalize_by_rowsum(message_embedding)
        return np.array(message_embedding)

    def sem_similarty_scoring(self, clusters):
        """
        Run biased PageRank using Universal Sentence Encoder to receive embedding.
        Calls add add_tp_ratio() and add_syn_similarity().
        Computes similarity to conclusion.
        :param clusters:
        :return:
        """
        # TODO modelling the context of argument
        # TODO Add more similar arguments in cluster

        messages = []
        for cluster in clusters:

            messages = cluster.sentences
            context_text = messages

            message_embedding = [message.numpy() for message in self.embed(context_text)]

            print(context_text)
            print('Sentences')
            print(messages)

            sim = np.inner(message_embedding, message_embedding)
            matrix = self.add_tp_ratio(messages)
            shape = np.shape(matrix)
            matrix_context = np.zeros(sim.shape)
            matrix_context[:shape[0], :shape[1]] = matrix
            # print(matrix.shape)
            print("Argumentative Score")
            print(matrix_context)

            M = np.array(sim) * (1 - self.d) + np.array(matrix_context) * self.d

            # print(M)

            # p = self.power_method(M, 0.0000001)
            mc = markovChain(M)
            mc.computePi('power')
            p = mc.pi

            print(p.shape)
            x = 0
            if not cluster.score:
                score_exists = False
            else:
                score_exists = True
            for j in range(len(cluster.sentences)):
                if score_exists:
                    cluster.score[j] += p[x]
                    cluster.score[j] = cluster.score[j]

                else:
                    cluster.score.append(p[x])
                x += 1
            if len(cluster.score) > 1:
                cluster.score = list(
                    (cluster.score - min(cluster.score)) / (
                            max(cluster.score) - min(cluster.score)))
            else:
                cluster.score = [1]

    def generate_snippet(self, args):

        output = []

        self.sem_similarty_scoring(args)
        for arg in args:
            arg_snippet = {}

            # processing snippet title
            snippet_title = arg.get_topK(1).tolist()[0]
            # snippet_title_span = self.find_span(arg_text, snippet_title)
            arg_snippet['id'] = arg.id
            arg_snippet['snippet-title'] = snippet_title

            # processing snippet body
            snippet_body_sentences = arg.get_topK(2).tolist()

            # snippet_body = []
            """
             sentence in snippet_body_sentences:
                try:
                    sentence_span = self.find_span(arg_text, sentence)
                    snippet_body.append({'span': sentence_span, 'text': sentence})
                except Exception as e:
                    print('Exection in sem_similarity score')
                    #self.flask_app.logger.error(str(e))
            """
            arg_snippet['snippets-text'] = snippet_body_sentences
            arg_snippet['aspects'] = arg.aspects
            arg_snippet['sentences'] = arg.premises

            output.append(arg_snippet)

        return output


def get_stored_snippets():
    script_dir = os.path.dirname(__file__)
    stored_snippets = json.load(open(os.path.join(script_dir, "../data/snippets.txt")))
    return stored_snippets
