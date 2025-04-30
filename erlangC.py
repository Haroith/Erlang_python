import math

class ErlangC:

    __lambda = None # calls forecast per 1 minute
    __beta = None # average handling time in minutes
    a = None # load in erlangs

    def __init__(self, calls_forecast_15_min, average_handling_time_seconds):
        self.__lambda = calls_forecast_15_min/15
        self.__beta = average_handling_time_seconds/60
        self.a = self.__load(self.__lambda, self.__beta)

    def __load(self, calls, average_handling_time) :
        load = calls * average_handling_time
        return load
    
    # s = number of agents
    def __sum_for_dp(self, s) :
        sum_for_dp = 0
        for j in range(s):
            sum_for_dp += self.a**j / math.factorial(j)
        return sum_for_dp

    # s = number of agents
    def __delay_probability(self, s) :
        delay_probability = (pow(self.a, s) / (math.factorial(s-1)*(s-self.a))) * pow(self.__sum_for_dp(s) + (pow(self.a, s)/(math.factorial(s-1)*(s-self.a))), -1);
        return delay_probability
    
    # s = number of agents
    # t = service level goal time in seconds
    def service_level_percents(self, s, t) :
        service_level_percents = 1 - self.__delay_probability(s) * math.exp(-1* (s/self.__beta-self.__lambda) * t)
        service_level_percents *= 100
        return service_level_percents

    # s = number of agents
    def average_speed_answer_seconds(self, s) :
        average_speed_answer_seconds = (self.__delay_probability(s) * self.__beta) / (s - self.a)
        return average_speed_answer_seconds

# We know calls forecast
# We want to achieve service level
# How many agents we need?
# Let's make functions for 15 minutes interval
# Using ErlangC formulae

calls_forecast_15_min = 47 # 47 calls per 15 minutes
service_level_percents_goal = 80 # 80%
service_level_time_goal = 20 # 20 seconds
# convert
service_level_time_goal_minutes = service_level_time_goal / 60

# ErlangC formulae work with queue, so SL=80%/20seconds.

# We need to know more statistics
average_handling_time_seconds = 120 # average handling time in seconds

# Prepare the data
erlang_c = ErlangC(calls_forecast_15_min, average_handling_time_seconds)

# Formula is too complex, we cannot revert it
# Now we have to 'guess' number of agents
# Minimum number of agents = load from ErlangC class
calculated_sl = 1
agents = math.ceil(erlang_c.a);
while calculated_sl < service_level_percents_goal :
    agents += 1
    calculated_sl = erlang_c.service_level_percents(agents, service_level_time_goal_minutes)

calculated_asa = erlang_c.average_speed_answer_seconds(agents)

print('required agents=',agents,'.')
print('resulted service level=',calculated_sl,'%')
print('resulted average speed of answer=',calculated_asa,' minutes')