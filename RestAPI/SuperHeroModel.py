import os
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer as VEC
from sklearn.preprocessing import normalize
import cPickle
import numpy as np

class Model(object):
    """
    Superhero prediction Model
    Features: TF/IDF vectorisation of hero-articles, vocabulary size 6000
    Classifier: Logistic Regression (with default L2 regularization)
    """
    def __init__(self, store):
        """
        args: 
        store -- an SHpersistence.SuperHeroStore instance 
        """
        self.store = store
        self.vecfile = 'hero_vectorizer.pkl'
        self.modelfilename = 'heromodel.pkl'
    
    def train(self):
        """
        Trains a new model from articles in database 
        """
        vec, model = self.__train_model()
        self.__save_model(vec, model)
    
    def predict(self, text):
        """
        Predicts the Superhero Universe from supplied text
        """
        vec, logreg = self.__load_model()
        features = self.__get_features(vec, [text])
        prediction = logreg.predict(features)
        return 'dc' if prediction < 0.5 else 'marvel'
    
    
    def __read_heros(self):
        texts = []
        labels = []
    
        for h in self.store.get_everything():
            texts.append(h['text'])
            labels.append(0 if h['dc_or_marvel']=='dc' else 1)
        
        return texts, np.array(labels)
    
    def __train_vectorizer(self, texts, vocabsize=6000):
        assert vocabsize > 0, 'vocabsize'
        vec = VEC(max_features=vocabsize, stop_words='english')
        vec.fit(texts)
        return vec
    
    def __get_features(self,vectorizer, texts):
        
        return normalize(vectorizer.transform(texts).toarray())
        
    def __get_newmodel(self, features, labels):
        logreg = LogisticRegression()
        logreg.fit(features, labels)
        return logreg
        
    def __train_model(self):
        texts, labels = self.__read_heros()
        vec = self.__train_vectorizer(texts)
        features = self.__get_features(vec, texts)
        model = self.__get_newmodel(features, labels)
        return vec, model

    def __save_model(self, vectorizer, model):
        with open(self.vecfile, 'w') as vecfile:
            cPickle.dump(vectorizer, vecfile)
        with open(self.modelfilename,'w') as modelfile:
            cPickle.dump(model, modelfile)
        
    def __load_model(self):
        _vec = None
        _logreg = None
        if not os.path.exists(self.modelfilename) or not os.path.exists(self.vecfile):
           _vec, _logreg = train_model()
           self.save_model(_vec,_logreg)
        with open(self.vecfile,'r') as vecfile:
            _vec = cPickle.load(vecfile)
        with open(self.modelfilename,'r') as modelfile:
            _logreg = cPickle.load(modelfile)
        
        return _vec, _logreg