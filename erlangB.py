class ErlangB:

    def __init__(self, calls, averageHandlingTime):
        self.calls = calls
        self.averageHandlingTime = averageHandlingTime
        self.erlangs = self.func_erlangs(self.calls, self.averageHandlingTime)

    def func_erlangs(self, calls, averageHandlingTime) :
        erlangs = calls * averageHandlingTime
        return erlangs
    
    def my_factorial(self, number):
        result = 1
        for i in range(number):
            result *= (i+1)
        return result
    
    def denominator_for_pb(self, agents) :
        denominator = 0
        for i in range(agents):
            denominator += (self.erlangs ** i / self.my_factorial(i))
        return denominator

    def probability_of_blocking(self, agents) :
        probabilityOfBlocking = ((self.erlangs**agents) / self.my_factorial(agents)) / self.denominator_for_pb(agents)
        return probabilityOfBlocking
    
# We know calls forecast
# We want to achieve service level
# How many agents we need?
# Let's make functions for 15 minutes interval
# Using ErlangB formulae

callsForecast = 47 # 47 calls
serviceLevelGoal = 80 # 80%

# ErlangB formulae work without queue, so SL=80, not 80/20.

# We need to know more statistics
aht = 63 # average handling time in seconds
aht = aht/60 # convert to minutes

# Prepare the data
erlang_b = ErlangB(callsForecast, aht);

# Now we have to 'guess' number of agents
calculatedSL = 1
agents = 0
while calculatedSL > (1-serviceLevelGoal/100) :
    agents += 1
    calculatedSL = erlang_b.probability_of_blocking(agents)

# converting to real SL
calculatedSL = round((1-calculatedSL)*100, 2);
print('required agents=', agents)
print('resulted service level=', calculatedSL, '%')
