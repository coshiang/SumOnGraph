from FullTextSum.pubmed_parser import pubmed_oa_parser
from nltk.tokenize import sent_tokenize, word_tokenize
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer,LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from FullTextSum.humumls.examples.aggregator import Aggregator

# Discard general concepts below
# STY     T079    Temporal Concept        A2.1.1
# STY     T080    Qualitative Concept     A2.1.2
# STY     T081    Quantitative Concept    A2.1.3
# STY     T169    Functional Concept      A2.1.4
# STY     T078    Idea or Concept A2.1
# STY     T082    Spatial Concept A2.1.5
# STY     T041    Mental Process  B2.2.1.1.1.1
# STY     T170    Intellectual Product    A2.4
# STY     T171    Language        A2.5

generic_sametype = ['A2.1.1' ,'A2.1.2', 'A2.1.3', 'A2.1.4','A2.1', 'A2.1.5', 'B2.2.1.1.1.1', 'A2.4', 'A2.5']
new1 = 'qnco'
class Preprocess(object):
    def __init__(self):
        self.parser = pubmed_oa_parser

    def read_file(self, file):
        str_file_path = file
        dict_paragraphs = self.parser.parse_pubmed_paragraph(str_file_path, True)
        return dict_paragraphs

    def get_word_list_from_paragraph(self, paragraph_list):
        word_list = []

        dict_phrases = {}
        i = 1
        for paragraph in paragraph_list:
            phrases = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)
            # phrases = sent_tokenize(paragraph)
            for phrase in phrases:
                phrase = re.sub(r'\[.*\]', '', phrase)
                dict_phrases[str(i)] = phrase
                words = word_tokenize(phrase)
                words = self.remove_duplicates(words)
                words = self.remove_stopwords(words)
                words = self.remove_numeric_special(words)
                words = self.stemming(words)
                word_list.append(words)
                i = i + 1
        return word_list, dict_phrases

    def get_word_list_from_sentence(self, sentence):
        word_list = []
        sentence = re.sub(r'\[.*\]', '', sentence)
        words = word_tokenize(sentence)
        words = self.remove_duplicates(words)
        words = self.remove_stopwords(words)
        words = self.remove_numeric_special(words)
        words = self.stemming(words)
        word_list.append(words)
        return word_list

    def remove_duplicates(self, values):
        output = []
        seen = set()
        for value in values:
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    def remove_stopwords(self, word_list):
        processed_word_list = []
        temp = ''
        for word in word_list:
            word = word.lower()  # in case they aren't all lower cased

            if word not in stopwords.words("english"):
                if not word.isdigit():
                    if word[-1:] == '-':
                        temp += word.replace('-', '')
                    else:
                        processed_word_list.append(temp+word)
                        temp = ''
        return processed_word_list

    def remove_numeric_special(self, word_list):
        processed_word_list = []
        for word in word_list:
            word = re.sub('[^A-Za-z0-9]+', '', word)
            if word != '' and not word.isdigit():
                processed_word_list.append(word)
        return processed_word_list

    def stemming(self, words):
        # ps = PorterStemmer()
        # ps = LancasterStemmer()
        ps = WordNetLemmatizer()
        stem_keyword_list = []
        for word in words:
            # stemword = ps.stem(word)
            stemword = ps.lemmatize(word)
            if stemword not in stem_keyword_list:
                stem_keyword_list.append(stemword)
        return stem_keyword_list

    def get_gold_standard(self, goldstd_paragraph_list):
        goldstd_list = list()
        for paragraph in goldstd_paragraph_list:
            phrases = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', paragraph)
            # phrases = sent_tokenize(paragraph)
            for phrase in phrases:
                phrase = re.sub(r'\[.*\]', '', phrase)
                goldstd_list.append(phrase)
        return goldstd_list

class Humumls(object):
    def __init__(self):
        self.agg = Aggregator()

    def get_cui(self, word_list):
        cui_temp_list = []
        for word in word_list:
            word_cui_list = self.agg.concepts_string(word)
            for cui in word_cui_list:
                if cui['_id'] not in cui_temp_list:
                    cui_temp_list.append(cui['_id'])
        return cui_temp_list

    def get_cui_specific(self, word_list):
        cui_temp_list = []
        for word in word_list:
            word_cui_list = self.agg.concepts_string(word)
            for cui in word_cui_list:
                if cui['_id'] not in cui_temp_list:
                    if len(set(cui['semtype']) & set(generic_sametype)) != len(set(cui['semtype'])):
                     cui_temp_list.append(cui['_id'])
        return cui_temp_list


