import sys, os
import numpy as np
import matplotlib.pyplot as plt
import pickle

PERIOD = 1000
Y_MIN = 0.095
Y_MAX = 0.115
class ResultWrapper:

    def __init__(self,filename):
        self.filename = filename
        self.avg_rt_list = []
        self.q_max_list = []
        self.time_list = []

    def add(self, avg_rt, q_max, time):
        self.avg_rt_list.append(avg_rt)
        self.q_max_list.append(q_max)
        self.time_list.append(time)

    def plot(self):
        avg_rt_list = np.array(self.avg_rt_list)
        time_list = np.array(self.time_list)
        q_max_list = np.array(self.q_max_list)


        plt.plot(time_list, avg_rt_list, label=self.filename)
        #axes = plt.gca()
        #axes.set_ylim([Y_MIN,Y_MAX])
        #plt.show()

    def combine(self, result):
        self.avg_rt_list += result.avg_rt_list
        self.q_max_list += result.q_max_list
        last_time = 0 if not len(self.time_list) else self.time_list[-1]
        t_list = [(each + last_time + PERIOD) for each in result.time_list]
        self.time_list += t_list



def readPickle(filename):
    with open(filename, 'rb') as read_file:
        fileContent = pickle.load(read_file)
    print ("Read pickle from %s" % filename)
    return fileContent

def writePickle(filename, content):
    with open(filename, 'wb') as write_file:
        pickle.dump(content, write_file)
    print ("Write pickle into '%s'" % filename)

def main(filenames):
    #results = []
    #out_filename = filenames[1].split('_')[0]
    out_filename =  (filenames[1].split('one')[0]+'one') if 'one' in filenames[1] else (filenames[1].split('random')[0]+'random')
    all_result = ResultWrapper(out_filename)
    for i in range(len(filenames)):
        filename = filenames[i]
        t_filename =  filename.split('one')[1].split('.')[0] if 'one' in filename else filename.split('random')[1].split('.')[0]
        out_filename += "_" + t_filename
        if os.path.isfile(filename):
            result = ResultWrapper(filename)

            pickle_filename = filename.split('.')[0] + '_result.pickle'
            if os.path.isfile(pickle_filename):
                result = readPickle(pickle_filename)
            else:
                print ("Cannot find previous result.")
                with open(filename, 'r') as result_file:
                    count = 0
                    total_rt = 0.0
                    avg_rt = 0.0

                    for line in result_file:
                        #print (line)
                        if (line[:8] == 'TIMESTEP'):
                            try:
                                count += 1
                                timestep = int(line.split('STEP ')[1].split(' ')[0])
                                state = line.split('STATE ')[1].split(' ')[0]
                                epsilon = line.split('EPSILON ')[1].split(' ')[0]
                                action = line.split('ACTION ')[1].split(' ')[0]
                                reward = float(line.split('REWARD ')[1].split(' ')[0])
                                q_max = float(line.split('Q_MAX ')[1].split(' ')[0])
                                if 'rm' in line:
                                    avg_rt = float(line.split('AVG RT ')[1].split(' ')[0])
                                    rm = line.split('rm: ')[1][0]
                                else:
                                    total_rt += reward
                                    avg_rt = total_rt / count
                                #print (timestep, state, epsilon, action, reward, q_max, avg_rt, rm)
                                if count % PERIOD == 0:
                                    print ("Timestep: ", count, "AVG_RT: ", avg_rt, end='\r')
                                    result.add(avg_rt, q_max, count)
                            except:
                                print (line)
                                stop = input("Error, press to continue ..")
                writePickle(pickle_filename, result)

            result.plot()
            #results.append(result)
            all_result.combine(result)

        else:
            print ("File", filename, "does not exists.")

    out_filename += "_result.pickle"
    writePickle(out_filename, all_result)
    plt.title("Result")
    plt.legend(loc=2)
    plt.xlabel("Number of Frame")
    plt.ylabel("AVG Reward: score = 1, nothig = 0.1, death = -1")
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Usage:", sys.argv[0], 'result files')
    else:
        main(sys.argv[1:])
