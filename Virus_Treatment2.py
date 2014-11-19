
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """

    TSTEP = 300
    result = 0
    res_sum = []
    avg = []
    for k in range(TSTEP):
        res_sum.append(0)
        

    for i in range(numTrials):
        
        # Create list of viruses
        virux = []
        
        for v in range(numViruses):
            virux.append(SimpleVirus(maxBirthProb, clearProb))
        
        Pat = Patient(virux,maxPop)
        
        #run sim on patient
        for k in range(TSTEP):
            Pat.update()
            result= Pat.getTotalPop()
            res_sum[k] = res_sum[k] +result

    for k in range(TSTEP):
        avg.append(float(res_sum[k])/float(numTrials))
       
    # Plotting after simulation
    pylab.plot(range(TSTEP), avg)
    pylab.title("SimpleVirus simulation")
    pylab.legend(('Trials','Average'))
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.show()      




