from math import log, log10
import numpy as np
import matplotlib.pyplot as plt

class AssetOptimizer():

    def __str__(self):
        return 'AssetOptimizer'

    def __init__(self, baseSalary, nYears, taxFunc, contribMaxima):
        self.baseSalary = float(baseSalary)
        self.nYears = int(nYears)
        self.rateFunc = rateFuncDecayed
        self.taxSchedule = applyIncomeTaxScheduleX
        self.taxFunc = taxFunc
        self.contribMaxima = contribMaxima

    def doOpt(self, type = 'Trad'):

        grosses = []        # Gross pay in year @year
        nets = []           # Net "take-home" pay in year @year ( == Gross - income taxes )
        contribs = []       # Amount contributed in year @year
        postContribs = []   # Net income post-contribution in year @year
        retirementAmts = [] # Retirement savings in year @year

        print("\nPre-retirement Years")
        print("year, growth, pretax, posttax, retirement savings")
        for year in range(self.nYears):

            rate, growth = self.rateFunc(year, self.nYears);
            grosses.append(self.baseSalary * growth);

            # Assumption: I will always contribute the maximum allowable amount
            contribs.append( self.contribMaxima[year] )

            # Can deduct traditional 401k contribution from taxable amount
            if 'Trad' == type:
                nets.append( grosses[year] - self.taxSchedule(grosses[year] - contribs[year]) )
            else: nets.append( grosses[year] - self.taxSchedule(grosses[year]) )

            postContribs.append( nets[year] -  contribs[year] )

            if year > 0:
                retirementAmts.append( applyInvestmentGrowth(retirementAmts[year-1], year) + contribs[year])
            else: retirementAmts.append( contribs[year] )

            print("%d %.4f %.2f %.2f %.2f %.2f" % (year+1, rate, grosses[year], 
                                              nets[year], postContribs[year], 
                                              retirementAmts[year]))

        return grosses, nets, postContribs, retirementAmts

    def runRetirement(self, savings, yearRetired = 40, yearsRetired = 30):
        
        annualDisbursement = savings / yearsRetired
        disbursementTax = self.taxFunc(annualDisbursement)

        grosses = []        # Gross disbursement
        nets = []           # Post-tax disbursement
        retirementAmts = [] # Remaining retirement savings

        print("\nRetirement Years")
        print("Year, Pretax, Posttax, Savings")
        for year in range(yearsRetired):

            grosses.append(annualDisbursement)
            nets.append(annualDisbursement - disbursementTax)

            if year > 0:
                retirementAmts.append( \
                    applyInvestmentGrowth(retirementAmts[year-1] - annualDisbursement, yearRetired+year) )
            else: retirementAmts.append(savings)

            print("%d %.2f %.2f %.2f" % (year+1, grosses[year], nets[year], retirementAmts[year]))

        return grosses, nets, retirementAmts

def applyInflation(amount, years, rate):
    return amount * (1 + rate)**years

def applyInvestmentGrowth(currentSavings, year):
    if year < 25:    return currentSavings*1.08 # 8% annual growth rate
    if year < 35:    return currentSavings*1.06 # 6%

    return currentSavings*1.03 # Very conservative 3%

 # N% first year growth with logarithmic decay
def rateFuncDecayed(year, period, baseGrowth = 5.):
    decay = 2*log10(year+1) / log10(period)
    rate = .01*(baseGrowth - decay)
    return rate, (1 + rate) ** year

 # 5% annual growth
def rateFuncConst(year, period):
    return 1.05**year

# Return tax owed for single filter on $ gross income @param income
def applyIncomeTaxScheduleX(income):

    tots = [0, 892.5, 4991.25, 17891.25, 44603.25, 115586.25, 116163.75]
    thres = [0, 8925, 36250, 87250, 183250, 398250, 400000]
    rates = [.1, .15, .25, .28, .33, .35, .396]

    if income < thres[1]:    return tots[0]      + rates[0]*(income-thres[0])
    if income < thres[2]:    return tots[1]      + rates[1]*(income-thres[1])
    if income < thres[3]:    return tots[2]      + rates[2]*(income-thres[2])
    if income < thres[4]:    return tots[3]      + rates[3]*(income-thres[3])
    if income < thres[5]:    return tots[4]      + rates[5]*(income-thres[4])
    if income < thres[6]:    return tots[5]      + rates[6]*(income-thres[5])

    return tots[6] + rates[7]*(income-thres[6])

def rothDisbTaxFunc(income):
    return 0.

def tradDisbTaxFunc(income):
    return applyIncomeTaxScheduleX(income)

def main():
    startAge = 24
    nWorkYears = 65-25
    nRetirementYears = 30

    totYears = nWorkYears + nRetirementYears

    years = range(1, totYears+1)
    baseSalary = 60000.

    contribMaximaRoth = [17500] # 2014
    contribMaximaTrad = [17500] # 2014
    
    # Predict contribution maximum increases
    for i in range(1, nWorkYears):
        if 0 == i % 3:    contribMaximaRoth.append(contribMaximaRoth[i-1]+500);
        else:             contribMaximaRoth.append(contribMaximaRoth[i-1]);

        if 0 == i % 3:    contribMaximaTrad.append(contribMaximaRoth[i-1]+500);
        else:             contribMaximaTrad.append(contribMaximaRoth[i-1]);

        # Apply catch-up contribution rules
        if 50 == startAge+i:
            contribMaximaRoth[i] += 5500;
            contribMaximaTrad[i] += 5500;

    print("\nRoth")
    ao = AssetOptimizer(baseSalary, nWorkYears, rothDisbTaxFunc, contribMaximaRoth)
    ao2 = AssetOptimizer(baseSalary, nWorkYears, tradDisbTaxFunc, contribMaximaTrad)

    grosses, nets, postContribs, retirementAmts = ao.doOpt(type = 'Roth')
    grosses2, nets2, retirementAmts2            = ao.runRetirement(retirementAmts[nWorkYears-1], \
                                                                   nWorkYears, 30);
    print("\nTraditional")
    grosses3, nets3, postContribs3, retirementAmts3 = ao2.doOpt(type = 'Trad')
    grosses4, nets4, retirementAmts4                = ao2.runRetirement(retirementAmts3[nWorkYears-1], \
                                                                        nWorkYears, 30);

    print("\nTotal income (Roth): %.2f" % ( sum(nets+nets2) ))
    print("Total income (Trad): %.2f" % ( sum(nets3+nets4) ))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(years, grosses+grosses2, '-', label = 'Gross Income')
    ax.plot(years, nets+nets2, '-', label = 'Income Post-Tax (Roth)')
    ax.plot(years, nets3+nets4, '-', label = 'Income Post-Tax (Trad)')
    ax.plot(years, postContribs+[nets2[0]]*30, '-', label = 'Income Post-Contribution (Roth)')
    ax.plot(years, postContribs3+[nets4[0]]*30, '-', label = 'Income Post-Contribution (Trad)')
    ax.set_xlim(1, totYears)
    ax.legend(loc=2)
    ax.grid()
    ax.set_xlabel("Year")
    ax.set_ylabel(r"USD")

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.plot(years, retirementAmts + retirementAmts2, label = '401(k) Assets (Roth)')
    ax2.plot(years, retirementAmts3 + retirementAmts4, label = '401(k) Assets (Trad)')
    ax2.set_xlim(1, totYears)
    ax2.legend(loc=0)
    ax2.grid()
    ax2.set_xlabel("Year")
    ax2.set_ylabel(r"USD")
    plt.show()

if "__main__" == __name__:
    main()