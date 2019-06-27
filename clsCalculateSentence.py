from gensim.models import KeyedVectors
from matplotlib import pyplot
from sklearn.decomposition import PCA
from gensim.models import Word2Vec
import numpy as np

class CalculateSentence:
    def __init__(self):
        # -- First Time Only
        # filename = '/Users/coshiang/Downloads/wikipedia-pubmed-and-PMC-w2v.bin'
        # model = KeyedVectors.load_word2vec_format(filename, binary=True)
        # # model.init_sims(replace=True)
        # model.syn0norm = model.syn0  # prevent recalc of normed vectors
        # model.save('SmallerFile')
        # -- First Time Only

        # MODEL SAVED INTO SMALLERFILE & NEXT LOAD FROM IT
        self.model = KeyedVectors.load('SmallerFile', mmap='r')

    def get_similarity(self, s1, s2):
        if len(s1) == 0 or len(s2) == 0:
            return 0
        # calculate distance between two sentences using WMD algorithm
        distance = self.model.wmdistance(s1, s2)

        # print('distance = %.3f' % distance)
        # convert distance to similarity min 0 - max 1
        similarity = 1./(1.+distance)
        # print('similarity = %.3f' % similarity)

        return distance,similarity

    def get_distance(self, s1, s2):
        if len(s1) == 0 or len(s2) == 0:
            return 0
        # calculate distance between two sentences using WMD algorithm
        distance = self.model.wmdistance(s1, s2)

        return distance

    def get_vector(self, sentence):
        vector = self.model.getvector(sentence)

    def get_pairwise_distance(self, docs):
        D = np.zeros((len(docs), len(docs)))
        for i in range(len(docs)):
            for j in range(len(docs)):
                if i == j:
                    continue  # self-distance is 0.0
                if i > j:
                    D[i, j] = D[j, i]  # re-use earlier calc
                D[i, j] = self.model.wmdistance(docs[i], docs[j])
        return D
