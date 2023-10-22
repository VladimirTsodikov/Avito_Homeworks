from collections.abc import Iterable


class CountVectorizer:
    def __init__(self):
        self.dict_word = {}
        self.list_count_words = list[list[int]]

    def get_feature_names(self) -> list:
        """Возвращает список уникальных слов, встретившихся
        во всех строках массива строк, переданных через функцию fit_transform()
        """
        return list(self.dict_word)

    def fit_transform(self, raw_documents: Iterable) -> list[list[int]]:
        """Составляет матрицу list_count_word размером NxM, 
        где N - число переданных строк (размер raw_documents),
        M - число уникальных слов во всём тексте. 
        Для этого составляется словарь уникальных слов. 
        При добавлении в словарь ключом является само слово, а значением - 
        размер словаря на текущий момент. Т.к. из словаря слова не удаляются,
        то значения в словаре будут уникальными - целые числа, начиная с нуля.
        Значения используются как индекс столбца в матрице list_count_words,
        соответствующего данному уникальному слову.
        """
        if not isinstance(raw_documents, Iterable):
            raise TypeError
        self.list_count_words = [[] for i in range(len(raw_documents))]
        for i in range(len(raw_documents)):
            for word in raw_documents[i].split():
                if word.lower() not in self.dict_word:
                    self.dict_word[word.lower()] = len(self.dict_word)
                    for counts in self.list_count_words:
                        counts.append(0)
                self.list_count_words[i][self.dict_word[word.lower()]] += 1

        return self.list_count_words


if __name__ == '__main__':
    corpus = [
     'Crock Pot Pasta Never boil pasta again',
     'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    test_1 = [
     'This is the first document.',
     'This document is the second document.',
     'And this is the third one.',
     'Is this the first document?',
    ]
    test_2 = [
     'Crock crock CrOck Crook',
     'Croook crook crook'
    ]
    test_3 = [
        'test test',
        'test'
    ]

    vectorizer = CountVectorizer()
    count_matrix = vectorizer.fit_transform(test_3)
    print(vectorizer.get_feature_names())

    print(count_matrix)
