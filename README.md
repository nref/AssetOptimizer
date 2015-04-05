# AssetOptimizer
Retirement Optimization with Python

A simulation of pre-retirement and post-retirement income and 401(k) growth.

![Image](../blob/master/ExampleRetirement.png?raw=true)
![Image](../blob/master/ExamplePreRetirement.png?raw=true)

Accounted for in the model is

- initial salary, 
- salary growth with a decaying growth rate, 
- contribution maximum increases 
	(both Traditional and Roth) 
	(assumed to be $500 every 3 years)
- US income tax schedules for a single filer
- catch-up contributions (currently allowed age 50+)
- A change in growth rate / risk toelrance as retirement approaches

Input is 

- base salary
	e.g. $60000
- the year the simulated person enters the workforce
	e.g. 24 
- the length of his or her career
	e.g. 65-24 = 41 years, 
- the length of retirment
	e.g. death at 95 with retirement at 65 
	= 30 years in retirment.
- Initial Roth and Traditional contribution maxima
	e.g. $17,500 for both Roth and Traditional in 2014

Output is given both as text and charts:

Income pre-retirement pre-and post-tax for Roth and Traditional 401(k).

401(k) assets in pre- and post-retirement years.