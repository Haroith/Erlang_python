import math

class ErlangA :
    ACCURACYFORABANDONS = 0.00001;
    __lambda = None # calls per minute
    __mu = None # service rate
    __O = None # individual abandonment rate
    __beta = None # averageHandlingTime in minutes
    a = None # load in erlangs

    def __init__(self, calls_forecast_15_min, average_handling_time_seconds, average_patience) :
        self.__lambda = calls_forecast_15_min/15
        self.__mu = 1/(average_handling_time_seconds/60) # /60? in minutes?
        self.__O = 1/average_patience
        self.__beta = average_handling_time_seconds/60
        self.a = self.__load_c(self.__lambda, self.__beta)
    
    def __load_c(self, calls, average_handling_time) :
        load = calls * average_handling_time
        return load
    
    # s = number of agents
    def __sum_for_dp(self, s) :
        sum_for_dp = 0
        for j in range(0, s):
            sum_for_dp += pow(self.a, j)/math.factorial(j)
        return sum_for_dp
    
    # s = number of agents
    def __delay_probability(self, s) :
        delay_probability = (pow(self.a, s) / (math.factorial(s-1)*(s-self.a))) * pow(self.__sum_for_dp(s) + (pow(self.a, s)/(math.factorial(s-1)*(s-self.a))), -1)
        return delay_probability
    
    # s = number of agents
    # t = service level goal time in seconds
    def service_level_percents(self, s, t) :
        service_level_percents = 1 - self.__delay_probability(s) * math.exp(-1* (s/self.__beta-self.__lambda) * t)
        service_level_percents *= 100
        return service_level_percents

    def __load(self, n) :
        load = self.__lambda/(n*self.__mu)
        return load
    
    def __a(self, x, y) :
        eternal_sum = 0
        previous_sum = -1
        j = 1
        while eternal_sum-previous_sum > self.ACCURACYFORABANDONS :
            previous_sum = eternal_sum
            denominator = 1
            for k in range(1, j + 1):
                denominator *= x + k
            eternal_sum += pow(y, j)/denominator
            j += 1
        return 1 + eternal_sum
    
    def ProbabilityOfAbandon(self, n) : 
        ro = self.__load(n) # load per agent
        probability_of_abandon = 1/(ro * self.__a(n*self.__mu/self.__O , self.__lambda/self.__O)) + 1 - 1/ro
        return probability_of_abandon
    

