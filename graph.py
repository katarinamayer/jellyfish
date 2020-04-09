import random

class Jellyfish():

    def __init__(self, numSwitches, numPorts):

        self.numPorts = numPorts
        self.numSwitches = numSwitches # switches are nodes here

        super(Jellyfish, self).__init__()

        switches = []
        ports = []
        for i in range(self.numSwitches):
            switches.append('s' + str(i))
            ports.append(self.numPorts) # each switch has all open ports at this point

        self.adjacent = self.build_graph(switches, ports)

    def build_graph(self, switches, ports):

        adjacent = set()

        while self.checkPossibleLinks(adjacent, ports):

            index1 = random.randrange(self.numSwitches)
            index2 = random.randrange(self.numSwitches)
            while (index2 == index1):
                index2 = random.randrange(self.numSwitches)

            if (ports[index1] > 0 and ports[index2] > 0):
                if ((index1, index2) not in adjacent):

                    ports[index1] -= 1
                    ports[index2] -= 1

                    adjacent.add((index1, index2))
                    adjacent.add((index2, index1))

        i = 0
        while i < self.numSwitches:
            if (ports[i] >= 2):
                #print("s"+str(i)+" has more than 2 ports.")
                randLink = random.choice(tuple(adjacent))

                if (randLink[0] == i or randLink[1] == i):
                    i += 0 # restart the loop to choose a new random link

                else:
                    #print("s"+str(i)+" has >= 2 ports. Link between "+str(randLink)+" broken. New links between "+str((i, randLink[0]))+" and "+str((i, randLink[1]))+" formed.")
                    adjacent.remove(randLink)
                    adjacent.remove((randLink[1], randLink[0]))

                    adjacent.add((i, randLink[0]))
                    adjacent.add((randLink[0], i))
                    adjacent.add((i, randLink[1]))
                    adjacent.add((randLink[1], i))
                    ports[i] -= 2
                    i += 1
            i+=1

        return adjacent

    def checkPossibleLinks(self, adjacent, ports):
        for i in range(self.numSwitches):
            if (ports[i] > 0):
                for j in range (self.numSwitches):
                    if (ports[j] > 0 and j != i):
                        if((i, j) not in adjacent):
                            return True
        return False


def main():
    return 0

if __name__ == '__main__':
    main()
