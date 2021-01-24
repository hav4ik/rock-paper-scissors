from kumoko.kumoko_base import BaseAtomicStrategy


class CentrifugalBumblepuppy16h(BaseAtomicStrategy):
  def __init__(self):
    self.code = compile("""
#see also www.dllu.net/rps.html
#Centrifugal Bumblepuppy + Helicase
import random
numPre = 60
numMeta = 18
if not his_move and not our_move:
	limits = [50,20,10]
	beat={'R':'P','P':'S','S':'R'}
	moves=['','','']
	pScore=[[3]*numPre,[3]*numPre,[3]*numPre,[3]*numPre,[3]*numPre,[3]*numPre]
	centrifuge={'RP':'a','PS':'b','SR':'c','PR':'d','SP':'e','RS':'f','RR':'g','PP':'h','SS':'i'}
	length=0
	p=[random.choice("RPS")]*numPre
	m=[random.choice("RPS")]*numMeta
	mScore=[3]*numMeta
	helicase=[0,0,0,0,0,0]
else:
	for i in range(numPre):
		pScore[0][i]=0.8*pScore[0][i]+((his_move==p[i])-(his_move==beat[beat[p[i]]]))*3
		pScore[1][i]=0.8*pScore[1][i]+((our_move==p[i])-(our_move==beat[beat[p[i]]]))*3
		pScore[2][i]=0.87*pScore[2][i]+(his_move==p[i])*3.3-(his_move==beat[p[i]])*0.9-(his_move==beat[beat[p[i]]])*3
		pScore[3][i]=0.87*pScore[3][i]+(our_move==p[i])*3.3-(our_move==beat[p[i]])*0.9-(our_move==beat[beat[p[i]]])*3
		pScore[4][i]=(pScore[4][i]+(his_move==p[i])*3)*(1-(his_move==beat[beat[p[i]]]))
		pScore[5][i]=(pScore[5][i]+(our_move==p[i])*3)*(1-(our_move==beat[beat[p[i]]]))
	for i in range(numMeta):
		mScore[i]=(mScore[i]+(his_move==m[i]))*(1-(his_move==beat[beat[m[i]]]))
	moves[0]+=centrifuge[his_move+our_move]
	moves[1]+=his_move
	moves[2]+=our_move
	length+=1
	for z in range(3):
		limit = min([length,limits[z]])
		for y in range(3):
			j=limit
			while j>=1 and not moves[y][length-j:length] in moves[y][0:length-1]:
				j-=1
			i = moves[y].rfind(moves[y][length-j:length],0,length-1)
			p[0+2*y+6*z] = moves[1][j+i]
			p[1+2*y+6*z] = beat[moves[2][j+i]]

	helicase[0] = helicase[0]*0.95+{'R':0,'P':-0.1,'S':0.1}[our_move]
	helicase[1] = helicase[1]*0.95+{'R':0.1,'P':0,'S':-0.1}[our_move]
	helicase[2] = helicase[2]*0.95+{'R':-0.1,'P':0.1,'S':0}[our_move]
	p[18] = {0:'R',1:'P',2:'S',3:'R',4:'P',5:'S'}[helicase.index(max(helicase[0:3]))]

	helicase[3] = helicase[3]*0.95+{'R':0.1,'P':0,'S':-0.1}[his_move]
	helicase[4] = helicase[4]*0.95+{'R':-0.1,'P':0.1,'S':0}[his_move]
	helicase[5] = helicase[5]*0.95+{'R':0,'P':-0.1,'S':0.1}[his_move]
	p[19] = {0:'R',1:'P',2:'S',3:'R',4:'P',5:'S'}[helicase.index(max(helicase[3:6]))]

	for i in range(20,20*3):
		p[i]=beat[beat[p[i-20]]]

	for i in range(0,6,2):
		m[i]=       p[pScore[i  ].index(max(pScore[i  ]))]
		m[i+1]=beat[p[pScore[i+1].index(max(pScore[i+1]))]]
	for i in range(6,18):
		m[i]=beat[beat[m[i-6]]]
output = beat[m[mScore.index(max(mScore))]]
if random.random()<0.13 or random.randint(3,40)>length:
	output =beat[random.choice("RPS")]
""", '<string>', 'exec')
    self.gg = {}

  def __call__(self, history):
      our_last_move, his_last_move = '', ''
      if len(history) > 0 \
          and history.his_moves[-1] is not None \
          and history.our_moves[-1] is not None:
        his_last_move = history.his_moves[-1]
        our_last_move = history.our_moves[-1]
      self.gg['his_move'] = his_last_move
      self.gg['our_move'] = our_last_move
      exec(self.code, self.gg)
      return self.gg['output']


class CentrifugalBumblepuppy4(BaseAtomicStrategy):
  def __init__(self):
    self.code = compile(
    """
#                         WoofWoofWoof
#                     Woof            Woof
#                Woof                      Woof
#              Woof                          Woof
#             Woof  Centrifugal Bumble-puppy  Woof
#              Woof                          Woof
#                Woof                      Woof
#                     Woof            Woof
#                         WoofWoofWoof

import random

number_of_predictors = 60 #yes, this really has 60 predictors.
number_of_metapredictors = 4 #actually, I lied! This has 240 predictors.


if not his_move and not our_move:
	limits = [50,20,6]
	beat={'R':'P','P':'S','S':'R'}
	urmoves=""
	mymoves=""
	DNAmoves=""
	outputs=[random.choice("RPS")]*number_of_metapredictors
	predictorscore1=[3]*number_of_predictors
	predictorscore2=[3]*number_of_predictors
	predictorscore3=[3]*number_of_predictors
	predictorscore4=[3]*number_of_predictors
	nuclease={'RP':'a','PS':'b','SR':'c','PR':'d','SP':'e','RS':'f','RR':'g','PP':'h','SS':'i'}
	length=0
	predictors=[random.choice("RPS")]*number_of_predictors
	metapredictors=[random.choice("RPS")]*number_of_metapredictors
	metapredictorscore=[3]*number_of_metapredictors
else:

	for i in range(number_of_predictors):
		#metapredictor 1
		predictorscore1[i]*=0.8
		predictorscore1[i]+=(his_move==predictors[i])*3
		predictorscore1[i]-=(his_move==beat[beat[predictors[i]]])*3
		#metapredictor 2: beat metapredictor 1 (probably contains a bug)
		predictorscore2[i]*=0.8
		predictorscore2[i]+=(our_move==predictors[i])*3
		predictorscore2[i]-=(our_move==beat[beat[predictors[i]]])*3
		#metapredictor 3
		predictorscore3[i]+=(his_move==predictors[i])*3
		if his_move==beat[beat[predictors[i]]]:
			predictorscore3[i]=0
		#metapredictor 4: beat metapredictor 3 (probably contains a bug)
		predictorscore4[i]+=(our_move==predictors[i])*3
		if our_move==beat[beat[predictors[i]]]:
			predictorscore4[i]=0
			
	for i in range(number_of_metapredictors):
		metapredictorscore[i]*=0.96
		metapredictorscore[i]+=(his_move==metapredictors[i])*3
		metapredictorscore[i]-=(his_move==beat[beat[metapredictors[i]]])*3
		
	
	#Predictors 1-18: History matching
	urmoves+=his_move
	mymoves+=our_move
	DNAmoves+=nuclease[his_move+our_move]
	length+=1
	
	for z in range(3):
		limit = min([length,limits[z]])
		j=limit
		while j>=1 and not DNAmoves[length-j:length] in DNAmoves[0:length-1]:
			j-=1
		if j>=1:
			i = DNAmoves.rfind(DNAmoves[length-j:length],0,length-1) 
			predictors[0+6*z] = urmoves[j+i] 
			predictors[1+6*z] = beat[mymoves[j+i]] 
		j=limit			
		while j>=1 and not urmoves[length-j:length] in urmoves[0:length-1]:
			j-=1
		if j>=1:
			i = urmoves.rfind(urmoves[length-j:length],0,length-1) 
			predictors[2+6*z] = urmoves[j+i] 
			predictors[3+6*z] = beat[mymoves[j+i]] 
		j=limit
		while j>=1 and not mymoves[length-j:length] in mymoves[0:length-1]:
			j-=1
		if j>=1:
			i = mymoves.rfind(mymoves[length-j:length],0,length-1) 
			predictors[4+6*z] = urmoves[j+i] 
			predictors[5+6*z] = beat[mymoves[j+i]]
	#Predictor 19,20: RNA Polymerase		
	L=len(mymoves)
	i=DNAmoves.rfind(DNAmoves[L-j:L-1],0,L-2)
	while i==-1:
		j-=1
		i=DNAmoves.rfind(DNAmoves[L-j:L-1],0,L-2)
		if j<2:
			break
	if i==-1 or j+i>=L:
		predictors[18]=predictors[19]=random.choice("RPS")
	else:
		predictors[18]=beat[mymoves[j+i]]
		predictors[19]=urmoves[j+i]

	#Predictors 21-60: rotations of Predictors 1:20
	for i in range(20,60):
		predictors[i]=beat[beat[predictors[i-20]]] #Trying to second guess me?
	
	metapredictors[0]=predictors[predictorscore1.index(max(predictorscore1))]
	metapredictors[1]=beat[predictors[predictorscore2.index(max(predictorscore2))]]
	metapredictors[2]=predictors[predictorscore3.index(max(predictorscore3))]
	metapredictors[3]=beat[predictors[predictorscore4.index(max(predictorscore4))]]
	
	#compare predictors
action = beat[metapredictors[metapredictorscore.index(max(metapredictorscore))]]
if max(metapredictorscore)<0:
	action = beat[random.choice(urmoves)]
""", '<string>', 'exec')
    self.gg = {}


  def __call__(self, history):
      our_last_move, his_last_move = '', ''
      if len(history) > 0 \
          and history.his_moves[-1] is not None \
          and history.our_moves[-1] is not None:
        his_last_move = history.his_moves[-1]
        our_last_move = history.our_moves[-1]
      self.gg['his_move'] = his_last_move
      self.gg['our_move'] = our_last_move
      exec(self.code, self.gg)
      return self.gg['action']


