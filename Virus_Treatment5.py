
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    TSTEP = 150
    result = 0
    result_resist = 0
    res_sum = []
    sum_resist = []
    avg = []
    avg_resist = []
    for k in range(2*TSTEP):
        res_sum.append(0)
        sum_resist.append(0)
    
    for i in range(numTrials):
        
        # Create list of viruses
        virux = []
        
        for v in range(numViruses):
            ###__init__(self, maxBirthProb, clearProb, resistances, mutProb)
            virux.append(ResistantVirus(maxBirthProb, clearProb,resistances, mutProb))
        
        Pat = TreatedPatient(virux,maxPop)
        
        #run sim on patient - part 1
        for k in range(TSTEP):
            Pat.update()
            result= Pat.getTotalPop()
            result_resist = Pat.getResistPop(['guttagonol'])
            res_sum[k] = res_sum[k] +result
            sum_resist[k] = sum_resist[k] +result_resist   
        #add the drugs
        Pat.addPrescription('guttagonol')
    
        #run sim on patient - part 2
        for k in range(TSTEP):
            Pat.update()
            result= Pat.getTotalPop()
            result_resist = Pat.getResistPop(['guttagonol'])
            res_sum[k+TSTEP] = res_sum[k+TSTEP] +result
            sum_resist[k+TSTEP] = sum_resist[k+TSTEP] +result_resist
    
    
    for k in range(2*TSTEP):
        avg.append(float(res_sum[k])/float(numTrials))
        avg_resist.append(float(sum_resist[k])/float(numTrials))
       
    # Plotting after simulation
    pylab.plot(range(2*TSTEP), avg)
    pylab.plot(range(2*TSTEP), avg_resist)
    pylab.title("ResistantVirus simulation")
    pylab.legend(('Trials','Average'))
    pylab.xlabel('Time Steps')
    pylab.ylabel('Average Virus Population')
    pylab.show()      
    