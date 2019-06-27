import networkx as nx


def create_graph(dict_pair, CUI_Word_list, CUI_keyword_list, blnWeight):
    dict_nodeWgCUI = {}
    default_wg = 1
    if blnWeight:
        # weight = getweight(CUI_TitleWord_list, CUI_keyword_list)
        # if weight > 0:
        #     dict_nodeWgCUI[str(0)] = weight

        if len(CUI_keyword_list) > 0:
            for i, iword_sentence in enumerate(CUI_Word_list, start=1):
                weight = getweight(iword_sentence, CUI_keyword_list)
                # if weight > 0:
                #     dict_nodeWgCUI[str(i)] = weight + default_wg
                dict_nodeWgCUI[str(i)] = weight + default_wg

        # max_wg = max(dict_nodeWgCUI.values())
        # min_wg = min(dict_nodeWgCUI.values())

        # for key, value in dict_nodeWgCUI.items():
        #     #normalized weight range 0-1
        #     dict_nodeWgCUI[key] = (value - min_wg)/(max_wg - min_wg)
    else:
        for i, iword_sentence in enumerate(CUI_Word_list, start=1):
            dict_nodeWgCUI[str(i)] = default_wg

    print(dict_nodeWgCUI.items())

    D = nx.DiGraph()

    # for key, value in dict_nodeWgCUI.items():
    #     D.add_node(key)
    #     D.node[key]['weight'] = value
    #     D.add_edge()
    for key, value in dict_pair.items():
        x = str(key)
        a, b = x.split('_')
        D.add_edge(a, b, weight=default_wg)

    for key, value in dict_nodeWgCUI.items():
        if key in D:
            D.node[key]['weight'] = value
            # outbound_list = D.out_edges(key)
            # if len(outbound_list) > 0:
            #     weightEdge = value  # value / len(outbound_list)
            #     for u, v in outbound_list:
            #         D.adj[u][v]['weight'] = weightEdge  # wg node

    # print(D.node)
    # print(D.edge)

    # Remve edge weight = 0
    for u, v in D.edges():
        if D.adj[u][v]['weight'] == 0:
            D.remove_edge(u, v)

    # Remove node that no edge
    remove = [node for node, degree in D.degree() if degree < 1]
    D.remove_nodes_from(remove)

    # print(D.edge)
    return D

def create_graphwg(dict_pair, CUI_Word_list, CUI_keyword_list, blnWeight):
    dict_nodeWgCUI = {}
    default_wg = 1
    if blnWeight:
        # weight = getweight(CUI_TitleWord_list, CUI_keyword_list)
        # if weight > 0:
        #     dict_nodeWgCUI[str(0)] = weight

        for i, iword_sentence in enumerate(CUI_Word_list, start=1):
            weight = getweight(iword_sentence, CUI_keyword_list)
            if weight > 0:
                dict_nodeWgCUI[str(i)] = (weight * 10) + default_wg

        # max_wg = max(dict_nodeWgCUI.values())
        # min_wg = min(dict_nodeWgCUI.values())

        # for key, value in dict_nodeWgCUI.items():
        #     #normalized weight range 0-1
        #     dict_nodeWgCUI[key] = (value - min_wg)/(max_wg - min_wg)

        print(dict_nodeWgCUI.items())

    D = nx.DiGraph()

    # for key, value in dict_nodeWgCUI.items():
    #     D.add_node(key)
    #     D.node[key]['weight'] = value
    #     D.add_edge()
    for key, value in dict_pair.items():
        x = str(key)
        a, b = x.split('_')
        # D.add_edge(a, b)
        D.add_edge(a, b, weight=default_wg)

    for key, value in dict_nodeWgCUI.items():
        if key in D:
            # D.node[key]['weight'] = value
            outbound_list = D.out_edges(key)
            if len(outbound_list) > 0:
                weightEdge = value  # value / len(outbound_list)
                for u, v in outbound_list:
                    D.adj[u][v]['weight'] = weightEdge # wg node

    # print(D.node)
    # print(D.edge)

    #**** Remove edge weight = 0
    thingsToChange = []
    for edge in D.edges():
        sign = D.get_edge_data(edge[0], edge[1])['weight']
        if sign == 0:
            thingsToChange.append(edge)

    for things in thingsToChange:
        D.remove_edge(things[0], things[1])
    # ****

    # for u, v in D.edges():
    #     if D.adj[u][v]['weight'] == 0:
    #         D.remove_edge(u, v)

    # Remove node that no edge
    remove = [node for node, degree in D.degree() if degree < 1]
    D.remove_nodes_from(remove)

    # print(D.edge)
    return D

def getweight(cui_word_list,cui_keyword_list):
    wg = 0
    # wg = len([x for x in cui_word_list if x in cui_keyword_list])
    wg = len(set(cui_word_list) & set(cui_keyword_list))
    return wg