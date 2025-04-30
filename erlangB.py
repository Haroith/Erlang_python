import math

class ErlangB:

    __erlangs = None;

    def __init__(self, calls, average_handling_time):
        self.__erlangs = self.__func_erlangs(calls, average_handling_time)

    def __func_erlangs(self, calls, average_handling_time) :
        erlangs = calls * average_handling_time
        return erlangs
    
    def __denominator_for_pb(self, agents) :
        denominator = 0
        for i in range(0, agents + 1):
            denominator += (self.__erlangs**i / math.factorial(i))
        return denominator

    def probability_of_blocking(self, agents) :
        probability_of_blocking = ((self.__erlangs**agents)/math.factorial(agents))/self.__denominator_for_pb(agents)
        return probability_of_blocking
    
# We know calls forecast
# We want to achieve service level
# How many agents we need?
# Let's make functions for 15 minutes interval
# Using ErlangB formulae

calls_forecast = 47 # 47 calls
service_level_goal = 80 # 80%

# ErlangB formulae work without queue, so SL=80, not 80/20.

# We need to know more statistics
aht = 63 # average handling time in seconds
aht = aht/60 # convert to minutes

# Prepare the data
erlang_b = ErlangB(calls_forecast, aht);

# Now we have to 'guess' number of agents
calculated_sl = 1
agents = 0
while calculated_sl > (1-service_level_goal/100) :
    agents += 1
    calculated_sl = erlang_b.probability_of_blocking(agents)

# converting to real SL
calculated_sl = round((1-calculated_sl)*100, 2);
print('required agents=', agents)
print('resulted service level=', calculated_sl, '%')
