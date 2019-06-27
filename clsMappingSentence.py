from FullTextSum.clsCalculateSentence import CalculateSentence


class MappingSentence:
    def __init__(self):
        self.cal = CalculateSentence()

    def mapping_one_cui(CUI_Word_list):
        # อันเดียวตรงกันก้อถือว่าเชื่อมกัน
        dict_pair = {}
        for i, iword_sentence in enumerate(CUI_Word_list, start=1):
            for iword in iword_sentence:
                for j, jword_sentence in enumerate(CUI_Word_list[i + 1:], start=i + 1):
                    # print(j, jword_sentence)
                    for jword in jword_sentence:
                        if iword == jword:
                            dict_pair[str(i) + '_' + str(j)] = True
                            continue
        return dict_pair

    def mapping_sentence(self, CUI_Word_list, word_list, dist_value):
        # ต้องตรงกัน ถ้า A --> B คือ cui ของ A ตรงกับ cui ของ B มากกว่า 50 percent A
        #     กลับกัน B --> A คือ cui ของ B ตรงกับ cui ของ A มากกว่า 50 percent B
        dict_pair = {}
        for i, iword_sentence in enumerate(CUI_Word_list, start=1):
            for j, jword_sentence in enumerate(CUI_Word_list[i:], start=i + 1):
                ilen = len(iword_sentence)
                jlen = len(jword_sentence)
                cnt = len(set(iword_sentence) & set(jword_sentence))
                # print(str(i-1) + '_' + str(j-1))

                if ilen == 0 or jlen == 0: continue

                # distance, similarity = self.cal.get_similarity(word_list[i-1], word_list[j-1])
                distance = self.cal.get_distance(word_list[i - 1], word_list[j - 1])

                # value = 0

                # if cnt >= ilen * 0.5:
                #     dict_pair[str(i) + '_' + str(j)] = 1
                # if cnt >= jlen * 0.5:
                #     dict_pair[str(j) + '_' + str(i)] = 1
                # if similarity >= 0.5:
                #     dict_pair[str(i) + '_' + str(j)] += 1
                #     dict_pair[str(j) + '_' + str(i)] += 1

                if cnt >= ilen * 0.5:
                    dict_pair[str(i) + '_' + str(j)] = True

                if cnt >= jlen * 0.5:
                    dict_pair[str(j) + '_' + str(i)] = True
                # if similarity >= 0.238133213:
                #     dict_pair[str(i) + '_' + str(j)] = True
                #     dict_pair[str(j) + '_' + str(i)] = True
                if distance <= dist_value:
                    dict_pair[str(i) + '_' + str(j)] = True
                    dict_pair[str(j) + '_' + str(i)] = True

        return dict_pair

    def mapping_cui_sentence(self, CUI_Word_list):
        # ต้องตรงกัน ถ้า A --> B คือ cui ของ A ตรงกับ cui ของ B มากกว่า 50 percent A
        #     กลับกัน B --> A คือ cui ของ B ตรงกับ cui ของ A มากกว่า 50 percent B
        dict_pair = {}
        for i, iword_sentence in enumerate(CUI_Word_list, start=1):
            for j, jword_sentence in enumerate(CUI_Word_list[i:], start=i + 1):
                ilen = len(iword_sentence)
                jlen = len(jword_sentence)
                cnt = len(set(iword_sentence) & set(jword_sentence))
                # print(str(i-1) + '_' + str(j-1))

                if ilen == 0 or jlen == 0 : continue

                if cnt >= ilen * 0.5:
                    dict_pair[str(i) + '_' + str(j)] = True
                if cnt >= jlen * 0.5:
                    dict_pair[str(j) + '_' + str(i)] = True

        return dict_pair

    def get_sentence_distance(self, word_list):
        dict_dist = {}
        dict_similar = {}
        for i, iword_sentence in enumerate(word_list, start=1):
            for j, jword_sentence in enumerate(word_list[i:], start=i + 1):
                # print('i = {} j = {}'.format(word_list[i-1], word_list[j-1]))
                if not word_list[i-1] or not word_list[j-1]:
                    distance = 100
                    similarity = 0
                else:
                    distance, similarity = self.cal.get_similarity(word_list[i-1], word_list[j-1])
                dict_dist[str(i) + '_' + str(j)] = distance
                dict_similar[str(i) + '_' + str(j)] = similarity
                print('{}, {}, {}'.format(str(i) + '_' + str(j), distance, similarity))
        return dict_dist, dict_similar

    def mapping_sentence_distance_fromdict(self, d, filename, dist_value, CUI_Word_list, word_list):
        # ต้องตรงกัน ถ้า A --> B คือ cui ของ A ตรงกับ cui ของ B มากกว่า 50 percent A
        #     กลับกัน B --> A คือ cui ของ B ตรงกับ cui ของ A มากกว่า 50 percent B
        dict_pair = {}
        for i, iword_sentence in enumerate(CUI_Word_list, start=1):
            for j, jword_sentence in enumerate(CUI_Word_list[i:], start=i + 1):
                ilen = len(iword_sentence)
                jlen = len(jword_sentence)
                cnt = len(set(iword_sentence) & set(jword_sentence))
                # print(str(i-1) + '_' + str(j-1))

                # if ilen == 0 or jlen == 0: continue

                distance = 0
                if filename in d:
                    if str(i) + '_' + str(j) in d[filename]:
                        distance = d[filename][str(i) + '_' + str(j)]

                # hasEdge = False
                if cnt >= ilen * 0.5:
                    dict_pair[str(i) + '_' + str(j)] = True
                    # hasEdge = True
                if cnt >= jlen * 0.5:
                    dict_pair[str(j) + '_' + str(i)] = True
                    # hasEdge = True
                # if (not hasEdge) and distance <= dist_value:
                #     dict_pair[str(i) + '_' + str(j)] = True
                #     dict_pair[str(j) + '_' + str(i)] = True
                if distance <= dist_value:
                    dict_pair[str(i) + '_' + str(j)] = True
                    dict_pair[str(j) + '_' + str(i)] = True

        return dict_pair

    def mapping_sentence_similar_fromdict(self, d, filename, sim_value, CUI_Word_list, word_list):
        # ต้องตรงกัน ถ้า A --> B คือ cui ของ A ตรงกับ cui ของ B มากกว่า 50 percent A
        #     กลับกัน B --> A คือ cui ของ B ตรงกับ cui ของ A มากกว่า 50 percent B
        dict_pair = {}
        for i, iword_sentence in enumerate(CUI_Word_list, start=1):
            for j, jword_sentence in enumerate(CUI_Word_list[i:], start=i + 1):
                ilen = len(iword_sentence)
                jlen = len(jword_sentence)
                cnt = len(set(iword_sentence) & set(jword_sentence))
                # print(str(i-1) + '_' + str(j-1))

                if ilen == 0 or jlen == 0: continue

                similarity = 0
                if filename in d:
                    if str(i) + '_' + str(j) in d[filename]:
                        similarity = d[filename][str(i) + '_' + str(j)]

                if cnt >= ilen * 0.5:
                    dict_pair[str(i) + '_' + str(j)] = True
                if cnt >= jlen * 0.5:
                    dict_pair[str(j) + '_' + str(i)] = True
                # if similarity >= sim_value:
                #     if ilen < jlen:
                #         dict_pair[str(i) + '_' + str(j)] = True
                #     elif ilen > jlen:
                #         dict_pair[str(j) + '_' + str(i)] = True
                #     else:
                #         dict_pair[str(i) + '_' + str(j)] = True
                #         dict_pair[str(j) + '_' + str(i)] = True
                if similarity >= sim_value:
                    if ilen < jlen:
                        dict_pair[str(j) + '_' + str(i)] = True
                    elif ilen > jlen:
                        dict_pair[str(i) + '_' + str(j)] = True
                    else:
                        dict_pair[str(i) + '_' + str(j)] = True
                        dict_pair[str(j) + '_' + str(i)] = True
        return dict_pair