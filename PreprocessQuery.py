from Lemmatizer import lemmatize_text
from Stopwords import all_stop_words
from PostingList import PostingList
import re


class PreprocessQuery:
 
    
    def __init__(self, query):
        self.query = query
        self.boolean2 = []
        self.stop_words = all_stop_words()
        self.lemmatize_text = lemmatize_text
        self.preprocessed_query = self.preprocess()
        
        
    


    def get_preprocessed_query(self):
        return self.preprocessed_query
        
        
    def preprocess(self):

        wildcard = []
        query = self.query
        query1 = query.split()

        # Boolean operators: + (OR), AND, NOT
        boolean_query = re.findall(r'\(|\)|\+|\bAND\b|\bOR\b|\bNOT\b|[^\s()+]+', query, flags=re.IGNORECASE)
        if any(word.upper() in ('AND', 'OR', 'NOT') or word == '+' for word in boolean_query):
            for word in boolean_query:
                if word.upper() in ('AND', 'OR', 'NOT'):
                    self.boolean2.append(word.upper())
                elif word in ('+', '(', ')'):
                    self.boolean2.append(word)
                else:
                    word = self.lemmatize_text(word.lower())[0][0]
                    self.boolean2.append(word)
            return [word for word in self.boolean2 if word not in ('AND', 'OR', 'NOT', '+', '(', ')')]
        
        if "*" in query:
            for i in query1:
                if '*' in i:
                    self.query = query.replace(i , '')
                    wildcard = self.wildcard(i)

        if ("AND" or "NOT") in query:
            self.boolean2 = query.split()
            for j in query1:
                if j == "AND" or j=="NOT":
                    query1.remove(j)
                    self.query = ','.join(query1) # مقدار عوض میشود و کوئری بدون عملگر های بولین وارد میشود
        
               
                    
        lemmatized_query = self.lemmatize_text(self.query)
        query = lemmatized_query[0]
        
        query = [q for q in query if q not in self.stop_words]
        # AND , NOT are not in stopword

        
        
        query.extend(wildcard)
        return query
    
    
    def wildcard(self , query):
        list1 = self.k_Gram(2 , query)
        w = PostingList()
        word_token = w.get_posting_list()
        
        word_list = []
        for key in word_token: 
           word_list.append(key)
        
           
           
        relevant_word = []
        for gram in list1:
            #if '$' in gram:
                #gram = gram.replace('$' , '')
            for key in word_list:
                if re.search(gram , key):
                    relevant_word.append(key)
        return relevant_word
            
    
 
    def k_Gram(self , k, text):
        k_list = []
        text = text.replace('*' , '')
        #k_list.append(("$") + text[0:k-1]) # تا ایندکس یکی کمتر از کا
        for i in range(len(text) - k + 1 ):
            k_list.append(text[i:i+k]) # چسباندن ایندکس آی تا یکی کمتر از آی + کا که این طور عمل میکند
        #k_list.append(text[i+1:] + ("$")) # در str عملگر پلاس و منها داریم
        return k_list



if __name__ == "__main__":
    m = PreprocessQuery("salam AND ali NOT reza")
    #print(m.boolean2)
    #n = PreprocessQuery("salam not ali")
    #t = PreprocessQuery("salam or ali")
    #z = PreprocessQuery("salam OR ali")
    #a = PreprocessQuery("salam or ali")
    #b = PreprocessQuery("salam or ali")
    #n = PreprocessQuery("salam and ali")
    #n = PreprocessQuery("salam AND ali")






        
    

