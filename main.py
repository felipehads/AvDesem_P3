import simpy

from aeroporto import Aeroporto

env = simpy.Environment()
aeroporto = Aeroporto(env)

env.process(aeroporto.processoGeralAeroporto(env))

env.run(until=300)