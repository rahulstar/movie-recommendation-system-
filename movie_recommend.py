# set of movies
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
                       'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
                       'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
                            'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
                            'You, Me and Dupree': 3.5}, 
           'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                              'Superman Returns': 3.5, 'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                            'The Night Listener': 4.5, 'Superman Returns': 4.0, 
                            'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 
                            'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                            'You, Me and Dupree': 2.0}, 
           'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                             'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt

def sim_distance(prefs, person1, person2):
    similarity = {}   
    
    for it in prefs[person1]:
        if it in prefs[person2]:
            similarity[it] = 1   
            
    if len(similarity) == 0: return 0  
    
    sum_of_sequares = sum([pow(prefs[person1][it] - prefs[person2][it], 2)
                           for it in similarity]) 
     
    return 1 / (1 + sum_of_sequares)

# http://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient
def sim_pearson(prefs, person1, person2):
    similarity = {}
    
    for it in prefs[person1]:
        if it in prefs[person2]:
            similarity[it] = 1
    
    n = len(similarity)
    if n == 0: return 0

    sum1 = sum([prefs[person1][it] for it in similarity])
    sum2 = sum([prefs[person2][it] for it in similarity])
    
    sum1_square = sum([pow(prefs[person1][it], 2) for it in similarity])
    sum2_square = sum([pow(prefs[person2][it], 2) for it in similarity])
    
    person_sum = sum([prefs[person1][it] * prefs[person2][it] for it in similarity])
    
    num = person_sum - (sum1 * sum2) / n
    den = sqrt((sum1_square - pow(sum1, 2)/n) * (sum2_square - pow(sum2, 2) / n))
     
    if den == 0: return 0
    
    return num / den

def getRecommendations(prefs, person, similarity = sim_distance):
    totals = {}
    simSums = {}
    
    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other)
        if sim <= 0: continue
        
        for it in prefs[other]:
            if it not in prefs[person] or prefs[person][it] == 0:
                totals.setdefault(it, 0)
                totals[it] += prefs[other][it] * sim
                simSums.setdefault(it, 0)
                simSums[it] += sim
        
    ranking = [(total / simSums[it], it) for it, total in totals.items()]
    ranking.sort()
    ranking.reverse()
    return ranking

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    return result

def topMatches(prefs, person, n = 5, similarity = sim_pearson):
    scores = [(similarity(prefs, person, other), other)
                    for other in prefs if other != person]
    scores.sort()
    scores.reverse()
    return scores[0:n]

    
def main():
    person1 = 'Lisa Rose'
    person2 = 'Gene Seymour'
    print sim_distance(critics, person1, person2)
    print sim_pearson(critics, person1, person2)
    print getRecommendations(critics, 'Toby', sim_pearson)
    print topMatches(critics, 'Toby', 3)
    print topMatches(critics, 'Toby', 3, sim_distance)
     
if __name__ == '__main__':
    main() 
