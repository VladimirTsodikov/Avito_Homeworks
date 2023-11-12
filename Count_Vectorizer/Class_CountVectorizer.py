from collections.abc import Iterable
from math import log


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

        >>> fit_transform(['Crock Pot Pasta Never boil pasta again',
          'Pasta Pomodoro Fresh ingredients Parmesan to taste')
        [[1, 1, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1]]
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


class TfidfTransformer:
    def __init__(self):
        pass

    @staticmethod  # т.к. результат работы не зависит от self
    def tf_transform(count_matrix: list[list[int]]) -> list[list[float]]:
        """term frequency (частота термина)
        Принимает список списков с количеством встреченных уникальных слов
        в каждой строке. Возвращает относительную частоту каждого уникального
        слова в каждом тексте

        >>> tf_transform([[1, 1, 2, 1, 0], [0, 2, 1, 2, 5]])
        [[0.2, 0.2, 0.4, 0.2, 0.0], [0.0, 0.2, 0.1, 0.2, 0.5]]
        """
        result = [[round(count_symb / sum(line), 3) for count_symb in line]
                  for line in count_matrix]
        return result

    @staticmethod
    def idf_transform(count_matrix: list[list[int]]) -> list[float]:
        """inverse document-frequency (логарифмированное отношение документов к частоте)
        Принимает список списков с количеством встреченных уникальных слов
        в каждой строке. Возвращает список со значениями
        ln((всего документов + 1) / (документов с данным словом + 1)) + 1
        для каждого уникального слова

        >>> idf_transform([[1, 1, 1, 0, 0], [0, 0, 1, 1, 1]])
        [[1.405, 1.405, 1.0, 1.405, 1.405]]
        """
        docs_count = len(count_matrix)
        result = []

        for row in zip(*count_matrix):
            counter = sum(int(num > 0) for num in row)
            result.append(log((docs_count + 1) / (counter + 1)) + 1)

        return result

    def fit_transform(self, count_matrix: list[list[int]]) -> list[list[float]]:
        """Возвращает tf*idf для переданной матрицы количества встреченных
        уникальных слов
        """
        tf = self.tf_transform(count_matrix)
        idf = self.idf_transform(count_matrix)
        result = []
        for line in tf:
            result.append([round(tf_el * idf_el, 3) for tf_el, idf_el in zip(line, idf)])
        return result


class TfidfVectorizer(CountVectorizer):
    def __init__(self):
        super().__init__()
        self.transformer = TfidfTransformer()

    def fit_transform(self, raw_documents: list[str]) -> list[list[float]]:
        """Принимает список строк. Преобразует в список списков из количества
        встреченных уникальных слов и находит для этой матрицы метрику td*idf
        """
        count_matrix_numders = super().fit_transform(raw_documents)
        return self.transformer.fit_transform(count_matrix_numders)


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
    count_matrix = vectorizer.fit_transform(test_1)
    print(vectorizer.get_feature_names())
    print(count_matrix)


    test_vectorizer = TfidfVectorizer()
    print(test_vectorizer.fit_transform(corpus))
    print(test_vectorizer.get_feature_names())
