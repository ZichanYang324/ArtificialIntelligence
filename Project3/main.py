import random

from FlightStatusNetwork import *
from Queries import *


class BayesianNetwork:
    def __init__(self, network):
        self.network = network
        self.vars = list(network.keys())

    def getProbability(self, variable, evidences):
        parentsValue = list()
        for parent in self.network[variable]["Parent"]:
            if parent in evidences:
                parentsValue.append(evidences[parent])
        parentsValue = tuple(parentsValue)
        p = self.network[variable]["Probability"][parentsValue]
        return p

    def extends(self, evidences, var, value):
        extended = dict(evidences)
        extended[var] = value
        return extended

    def equals(self, sample, evidences):
        for k, v in evidences.items():
            if sample[k] != v:
                return False
        return True

    def priorSample(self):
        sample = dict()
        for variable in self.vars:
            p = self.getProbability(variable, sample)
            sample[variable] = True if random.random() < p else False
        return sample

    def normalize(self, distribution):
        ans = list()
        for p in distribution:
            ans.append(p / sum(distribution))
        return ans

    def enumerationAsk(self, query, evidences):
        def enumerateAll(vars, evidences):
            if len(vars) == 0:
                return 1.0
            var = vars[0]
            if var in evidences:
                value = evidences[var]
                p = self.getProbability(var, evidences)
                p = p if value else 1 - p
                return p * enumerateAll(vars[1:], evidences)
            else:
                ans = 0
                for value in [True, False]:
                    p = self.getProbability(var, evidences)
                    p = p if value else 1 - p
                    ans += p * enumerateAll(vars[1:], self.extends(evidences, var, value))
                return ans
        result = list()
        result.append(enumerateAll(self.vars, self.extends(evidences, query, True)))
        result.append(enumerateAll(self.vars, self.extends(evidences, query, False)))
        return self.normalize(result)

    def rejectionSampling(self, query, evidences, number):
        valueCount = {True: 0, False: 0}
        while number > 0:
            sample = self.priorSample()
            if self.equals(sample, evidences):
                valueCount[sample[query]] += 1
            number -= 1
        result = [valueCount[True], valueCount[False]]
        return self.normalize(result)

    def markovBlanket(self, query, evidences):
        p = self.getProbability(query, evidences)
        pt = p
        pf = 1 - p
        evidences[query] = True
        for c in self.network[query]["Child"]:
            pc = self.getProbability(c, evidences)
            pc = pc if evidences[c] else 1 - pc
            pt *= pc
        evidences[query] = False
        for c in self.network[query]["Child"]:
            pc = self.getProbability(c, evidences)
            pc = pc if evidences[c] else 1 - pc
            pf *= pc
        return self.normalize([pt, pf])[0]

    def gibbsAsk(self, query, evidences, sampleNumber):
        sampleCount = {True: 0, False: 0}
        sample = self.priorSample()
        nonEvidence = list()
        for v in self.vars:
            if v in evidences:
                sample[v] = evidences[v]
            else:
                nonEvidence.append(v)
        for i in range(sampleNumber):
            temp = list(nonEvidence)
            while len(temp):
                random_var = random.choice(temp)
                temp.remove(random_var)
                p_mb = self.markovBlanket(random_var, sample)
                p = random.random()
                sample[random_var] = False if p > p_mb else True
            sampleCount[sample[query]] += 1
        distribution = [sampleCount[True], sampleCount[False]]
        return self.normalize(distribution)

if __name__ == "__main__":
    network = BayesianNetwork(flightStatusNetwork)
    for q in test_queries:
        query = q["Query"]
        evidences = q["Evidences"]
        print("Query:              {}".format(query))
        print("Evidences:          {}".format(evidences))
        print("Exact Inference:    {}".format(network.enumerationAsk(query, evidences)))
        print("Rejection Sampling: {}".format(network.rejectionSampling(query, evidences, 200000)))
        print("Gibbs Sampling:     {}".format(network.gibbsAsk(query, evidences, 200000)))
    