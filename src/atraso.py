from sklearn.linear_model import LogisticRegression
from sklearn import metrics

class TempoDeAtraso():
    def __init__(self, rota):
        self.rota = rota
        self.model = LogisticRegression()

    def treinar(self):
        dataset = self.getDataSet()
        self.model.fit(dataset['data'], dataset['target'])

    def getDataSet(self):
        dataset = {'data' : [], 'target': []}
        with open('./dataset/'+ self.rota +'.csv','r') as data:
            for line in data.readlines():
                aux = [int(value) for value in line.replace('\n','').split(',')]
                dataset['data'].append(aux[:-1])
                dataset['target'].append(aux[-1])

        return dataset

    def prever(self, dia, hora, fluxo):
        return self.model.predict([[dia, hora, fluxo]])[0]

    def __repr__(self):
        return "Rota: " + self.rota

if __name__ == "__main__":
    dt = TempoDeAtraso('1')
    dt.treinar()
    print(dt.prever(4,5,3))
