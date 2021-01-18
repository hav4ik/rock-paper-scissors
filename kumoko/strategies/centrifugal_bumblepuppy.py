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
