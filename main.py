from CosineSimilarity import CosineSimilarity

if __name__ == '__main__':
    query = input("Enter your query: ")
    cs = CosineSimilarity(query)
    print("QUERY 1 : ", query)
    try:
        print(cs.get_similar_documents())
    except ValueError as e:
        print(e)
    print()


 