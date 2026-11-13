# calculate cosine similarity between query and document
from tfidf import tfidf
from PreprocessQuery import PreprocessQuery
from PostingList import PostingList

class CosineSimilarity:
    
    #tf_idf docs and query
    
    def __init__(self, query):
        # tfidf = tfidf()
        # tfidf.get_tfidf_weights()
        self.tf_idf = tfidf()
        self.tf_idf.get_tfidf_weights() # برای داکیومنت
        self.tfidf = self.tf_idf.tfidf_wts # تمیز شده وزن های داکیومنت
        # print(self.tfidf)
        self.query = query# داکیومنت ها را در بخش تی اف آی دی اف گرفیتم و وزنشان را اوکی کردیم و اینجا نممیگیریم ولی برای کوئری چون پیش پردازش میخواد اوئل خود کوئری را میگیریم بعد لماتیزیشن به تی اف آی دی اف میفرستیم
        self.preprocess_query = PreprocessQuery(self.query)
        self.preprocessed_query = self.preprocess_query.get_preprocessed_query()
        if self.preprocess_query.boolean2:
            self.query_tfidf = {}  # Boolean search does not need query weights
        else:
            self.query_tfidf = self.tf_idf.query_tfidf(self.preprocessed_query) # برای کوئری که لما ها یا توکن های کوئری را به تی اف آی دی اف میفرستیم نه خودکلمات کوئری که پیش پردازش نشده اند
        # print(self.query_tfidf)
        self.N = self.tf_idf.get_N()
        pl = PostingList()
        # pl.get_posting_list()
        self.file_index = pl.get_file_index()
        # print("File Index: ", self.file_index)
        # print(self.N)
        self.boolean = self.preprocess_query.boolean2
        
    def check_boolean(self , query):

        # NOT is evaluated first, then AND, then + (OR)
        all_docs = set(self.file_index.keys())
        position = 0

        def read_not():
            nonlocal position
            if position >= len(query):
                raise ValueError('Incomplete Boolean query')

            word = query[position]
            position += 1

            if word == 'NOT':
                return all_docs - read_not()
            if word == '(':
                result = read_or()
                if position >= len(query) or query[position] != ')':
                    raise ValueError('Missing closing parenthesis')
                position += 1
                return result
            if word in ('AND', 'OR', '+', ')'):
                raise ValueError('Invalid Boolean query')

            if word in self.tfidf:
                return set(self.tfidf[word][1].keys())
            return set()

        def read_and():
            nonlocal position
            result = read_not()
            while position < len(query) and query[position] in ('AND', 'NOT'):
                if query[position] == 'AND':
                    position += 1
                # "sport NOT line" is treated like "sport AND NOT line"
                result = result & read_not()
            return result

        def read_or():
            nonlocal position
            result = read_and()
            while position < len(query) and query[position] in ('+', 'OR'):
                position += 1
                result = result | read_and()
            return result

        result = read_or()
        if position != len(query):
            raise ValueError('Invalid Boolean query')

        return [self.file_index[i] for i in sorted(result)]

    def cosine_similarity(self, query, doc):
        
        sum = 0
        query_scores = []
        for key in query:
            query_scores.append(query[key]) # مقدار وزن ها را میآوریم فقط
        for i in range(len(query)):
            sum += query_scores[i] * doc[i] # خط به خط ترم های کوئری را وزنشان را به وزن های ترم های داکیومنت ضرب میکنیم و جمع میکنیم تا معیار شباهت برای یک داکیومنت مرتبط بیاید
        return sum
    
    def get_all_docs(self):
        self.possible_relevant_docs = {}
        # print(self.preprocessed_query)
        i = int(0)
        for q in self.preprocessed_query: # هرکدوم از توکن های لما شده کوئری
            if q in self.tfidf: # چک بودن توکن کوئری در وزن امتیاز های داکیومنت ها
                dic = self.tfidf[q][1] # از داخل وزن های داکیومنت ها خود کوئری و تی اف ای دی اف های داکیومنت ها برای این توکن که در ایندکس متغیر کیو خود توکن کلمه است و در ایندکس 1 وزن های داکیومننت های مربوطه است که وزن ها و شماره داکیومنت مربوطه داخل این داکیومنت مقدار میدهیم
                for key in dic:
                    if key in self.possible_relevant_docs:
                        self.possible_relevant_docs[key][i] = dic[key]
                    else:
                        self.possible_relevant_docs[key] = [0] * len(self.preprocessed_query)
                        self.possible_relevant_docs[key][i] = dic[key]
            i += 1
        # print("Possible Rel. Docs: ", self.possible_relevant_docs)



    def get_similar_documents(self, n=10): #  n is top k
        
        if self.boolean :
            return self.check_boolean(self.boolean)
        else:
            self.get_all_docs()
            self.similar_documents = {}
            for doc in self.possible_relevant_docs:
                self.similar_documents[doc] = self.cosine_similarity(self.query_tfidf, self.possible_relevant_docs[doc])
            self.similar_documents = sorted(self.similar_documents.items(), key=lambda x: x[1], reverse=True)
            doc_name = []
            for key in self.similar_documents:
                doc_name.append(self.file_index[key[0]])
            if len(doc_name) < n:
                return doc_name
            return doc_name[:n]
    

if __name__ == '__main__':
    query = 'profitable venture computer'
    print("Query = ", query)
    cosine_similarity = CosineSimilarity(query)
    print(cosine_similarity.get_similar_documents())