# Get Files path
# Loop Read File
# Get Plain Text from file and separate to word
# Loop Word and find CUI from UMLS by humumls
# Create Graph
# Calculate and select important sentence
# Measurement by ROUGE
# Keep log
import glob
import networkx as nx
from FullTextSum.clsPreprocessDoc import Preprocess, Humumls
from FullTextSum.clsMappingSentence import MappingSentence
from FullTextSum.clsCreateGraph import create_graph
from FullTextSum.pythonrouge.pythonrouge import Pythonrouge
from pprint import pprint
import operator
import math

data_dir_in_str = '/Users/coshiang/Downloads/DatasetDemo/orixml1/'

m_intCompress = 90
m_semtype_sp = False

m_dis_value = 4.5

if __name__ == '__main__':
    file_list = list()
    dict_scores_list = list()
    file_name_list = list()

    for filename in glob.iglob(data_dir_in_str + '*.nxml'):
        file_list.append(filename)

    file_list = sorted(file_list)

    pre_precess = Preprocess()
    humumls = Humumls()
    mapping = MappingSentence()

    num_file = 0

    for file_path in file_list:
        try:
            num_file += 1
            print('file no. {}'.format(num_file))
            print(file_path)
            file_name = 'PMC'
            dict_paragraphs = pre_precess.read_file(file_path)

            goldstd_paragraph_list = list()
            goldstd_list = list()
            paragraph_list = list()
            conclusion_list = list()

            for paragraph in dict_paragraphs:
                if paragraph['section'] == 'abstract':
                    goldstd_paragraph_list.append(paragraph['text'])
                    file_name += str(paragraph['pmc'])
                elif paragraph['section'] == 'Conclusions':
                    conclusion_list.append(paragraph['text'])
                else:
                    paragraph_list.append(paragraph['text'])

            paragraph_list = paragraph_list + conclusion_list
            word_list, dict_phrases = pre_precess.get_word_list_from_paragraph(paragraph_list)

            text_original = ''
            for key, value in dict_phrases.items():
                text_original += '\n' + str(key) + '. ' + dict_phrases[key]

            goldstd_list = pre_precess.get_gold_standard(goldstd_paragraph_list)

            CUI_keyword_list = list()
            cui_word_list = list()
            i = 0
            for words in word_list[i:]:
                i = i + 1
                if m_semtype_sp:
                    cui_word = humumls.get_cui_specific(words)
                else:
                    cui_word = humumls.get_cui(words)
                cui_word_list.append(cui_word)

            dict_pair = mapping.mapping_sentence(cui_word_list, word_list, m_dis_value)

            D = create_graph(dict_pair, cui_word_list, CUI_keyword_list, False)

            print('Gold Standard')
            print(''.join(goldstd_list))

            intNumTop = math.ceil(len(dict_phrases) * (100 - m_intCompress) / 100)
            print('summary : {} sentences from {}'.format(str(intNumTop), str(len(dict_phrases))))

            # ------------------------- Page Rank -------------------
            dict_rank = nx.pagerank(D)
            sorted_x = dict(sorted(dict_rank.items(), key=operator.itemgetter(1), reverse=True)[:intNumTop])
            result_list = list()
            print('PageRank Summary')
            for key, value in sorted_x.items():
                print(dict_phrases[key])
                result_list.append(dict_phrases[key])

            summary = [result_list]  # summary: double list
            reference = [[goldstd_list]]  # reference: triple list

            rouge = Pythonrouge(summary_file_exist=False,
                                summary=summary, reference=reference,
                                n_gram=1, ROUGE_SU4=False, ROUGE_L=True,
                                recall_only=False, stemming=True, stopwords=True,
                                word_level=True, length_limit=False,
                                use_cf=False, cf=95, scoring_formula='best',
                                resampling=True, samples=1000, favor=True, p=0.5)
            score = rouge.calc_score()
            print('PageRank ROUGE Score')
            pprint(score)
            # ------------------------- Betweenness centrality -------------------

            dict_rank = nx.betweenness_centrality(D)
            sorted_x = dict(sorted(dict_rank.items(), key=operator.itemgetter(1), reverse=True)[:intNumTop])
            result_list = list()
            print('Betweenness centrality Summary')
            for key, value in sorted_x.items():
                print(dict_phrases[key])
                result_list.append(dict_phrases[key])

            summary = [result_list]  # summary: double list
            reference = [[goldstd_list]]  # reference: triple list

            rouge = Pythonrouge(summary_file_exist=False,
                                summary=summary, reference=reference,
                                n_gram=1, ROUGE_SU4=False, ROUGE_L=True,
                                recall_only=False, stemming=True, stopwords=True,
                                word_level=True, length_limit=False,
                                use_cf=False, cf=95, scoring_formula='best',
                                resampling=True, samples=1000, favor=True, p=0.5)
            score = rouge.calc_score()
            print('betweenness_centrality ROUGE Score')
            pprint(score)
            # -------------------------------- closeness_centrality ------------------------------------------
            dict_rank = nx.closeness_centrality(D)
            sorted_x = dict(sorted(dict_rank.items(), key=operator.itemgetter(1), reverse=True)[:intNumTop])
            result_list = list()
            print('Closeness centrality Summary')
            for key, value in sorted_x.items():
                print(dict_phrases[key])
                result_list.append(dict_phrases[key])

            summary = [result_list]  # summary: double list
            reference = [[goldstd_list]]  # reference: triple list

            rouge = Pythonrouge(summary_file_exist=False,
                                summary=summary, reference=reference,
                                n_gram=1, ROUGE_SU4=False, ROUGE_L=True,
                                recall_only=False, stemming=True, stopwords=True,
                                word_level=True, length_limit=False,
                                use_cf=False, cf=95, scoring_formula='best',
                                resampling=True, samples=1000, favor=True, p=0.5)
            score = rouge.calc_score()
            print('closeness_centrality ROUGE Score')
            pprint(score)
            # -------------------------------- closeness_centrality ----------------------------------------

            # -------------------------------- degree_centrality ------------------------------------------
            dict_rank = nx.degree_centrality(D)
            sorted_x = dict(sorted(dict_rank.items(), key=operator.itemgetter(1), reverse=True)[:intNumTop])
            result_list = list()
            print('Degree centrality Summary')
            for key, value in sorted_x.items():
                print(dict_phrases[key])
                result_list.append(dict_phrases[key])

            summary = [result_list]  # summary: double list
            reference = [[goldstd_list]]  # reference: triple list

            rouge = Pythonrouge(summary_file_exist=False,
                                summary=summary, reference=reference,
                                n_gram=1, ROUGE_SU4=False, ROUGE_L=True,
                                recall_only=False, stemming=True, stopwords=True,
                                word_level=True, length_limit=False,
                                use_cf=False, cf=95, scoring_formula='best',
                                resampling=True, samples=1000, favor=True, p=0.5)
            score = rouge.calc_score()
            print('degree_centrality ROUGE Score')
            pprint(score)
            # -------------------------------- degree_centrality ----------------------------------------

        except Exception as e:
                print('Generate Error at ' + file_name)
                print('Error:', e)
                continue
