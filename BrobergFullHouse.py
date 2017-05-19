"""
inputs = RMSfulllist.csv

This is combined Broberg Full House script
version = 1.5, August, 2016

Idea is to combine and simplify:
    - work for all semesters (identify when summer and when fall...)
    - merge all concepts into workable classes for better functionality
    - totality of modifications that ever need to be made by CO Matrons and Patrons are just in the top section
    - get rid of excessive printing
    - eventually print errors to the csv file?
"""

RMSlistname = 'RMSfulllist.csv'

#--------------------------------------
# THIS is Section For Betsy and Kyle
#       To edit when neccessary
#--------------------------------------
#notes:
# (fencap) gives capacity of each room in Fenwick.
#       (fen_possible_share) is list of rooms that are allowed to be shared (can be 1 or 2 people)
# (roccap) put capacity of each in Rochdaleroom. No exceptions for sharing exists here.
# (nsc_studios) is list of studios at NSC which can only have 1 person.
#        (nsc_otherrooms) is list of all rooms that are not studios (and can therefore have either 1 or 2 people)

fencap = {'01': 3, '02': 3, '03': 3, '04': 4, '05': 1, '06': 2, '07': 4, '08': 4, '09': 1, '10': 3,
          '11': 4, '12': 2, '13': 2, '14': 2, '15': 2, '16': 3, '17': 3, '18': 3, '19': 4, '20': 4,
          '21': 1, '22': 2, '23': 4, '24': 1, '25': 4, '26': 1, '27': 2, '28': 4, '29': 4,
          '31': 3, '32': 4, '33': 2, '34': 2, '35': 2, '36': 2}
fen_possible_share = ['05','09','21','24','26']
roccap = {'A10':1,'A11':1,'A12':3,'A13':4,'A14':4,'A15':4,'A16':4,'A20':3,'A30':2,'A31':2,'A32':3,'A33':3,'A34':3,
          'A40':1,'A41':2,'A42':1,'B10':4,'B11':4,'B12':4,'B13':4,'B14':4,'B15':3,'B16':1,'B17':1,'B20':3,'B21':4,
          'B30':2,'B31':2,'B32':3,'B33':3,'B34':3,'B35':4,'B40':1,'B41':2,'B42':2,'C10':1,'C11':1,'C12':4,'C13':4,
          'C14':4,'C15':4,'C30':3,'C31':3,'C32':2,'C33':2,'D10':1,'D11':1,'D12':3,'D13':4,'D14':4,'D15':4,'D16':3,
          'D20':3,'D30':2,'D31':2,'D32':3,'D33':3,'D34':3,'D40':1,'D41':2,'D42':2,'D43':1,'E10':4,'E11':4,'E12':4,
          'E13':4,'E14':4,'E15':1,'E16':1,'E17':3,'E20':4,'E21':3,'E30':4,'E31':3,'E32':3,'E33':3,'E34':2,'E35':2,
          'E40':2,'E41':2,'F10':3,'F11':1,'F12':1,'F13':4,'F14':4,'F15':4,'F16':4,'F20':3,'F30':3,'F31':3,'F32':3,
          'F33':2,'F34':2,'F40':1,'F41':2,'F42':1}
nsc_studios = [3, 9, 10]
nsc_otherrooms = [1,2,4,5,6,7,8,2526,2528,2530,2532,2534,2535]

#house info contains all information about house capacities (including the above defined lists)
#Example: if ACA can only host 50 now, below change  ('cap':56) to ('cap':50) in the 'ACA' row
#   for HIP  'partialcap' you give number of sts and lgs allowed
houseinfo = {
    'ACA': {'building': 'Andres Castro Arms', 'cap': 55,'gquota':{'m':30,'f':25}},
    'PRO': {'building': 'African American Theme House', 'cap': 21,'gquota':{'m':11,'f':10}},
    'CAZ': {'building': 'Casa Zimbabwe', 'cap': 105,'gquota':{'m':58,'f':47}},
    'CLO': {'building': 'Cloyne Court', 'cap': 119,'gquota':{'m':69,'f':50}},
    'CON': {'building': 'Convent', 'cap': 25,'gquota':{'m':15,'f':10}},
    'DAV': {'building': 'Davis House', 'cap': 36,'gquota':{'m':23,'f':13}},
    'EUC': {'building': 'Euclid Hall', 'cap': 21,'gquota':{'m':11,'f':10}},
    'FEN': {'building': 'Fenwick Weavers Village', 'partialcap': fencap,'poss_share':fen_possible_share}, #no gquota?
    'HIP': {'building': 'Hillegass Parker', 'partialcap': {'sts': 9, 'lgs': 16}}, #no gquota?
    'HOY': {'building': 'Hoyt Hall', 'cap': 60,'gquota':{'m':12,'f':48},'NONSUMgquota':{'f': 60}}, #Gquota changes over summer...
    'KID': {'building': 'Kidd Hall', 'cap': 17,'gquota':{'m':12,'f':5}},
    'KNG': {'building': 'Kingman Hall', 'cap': 46,'gquota':{'m':23,'f':23}},
    'LOT': {'building': 'Lothlorien', 'cap': 58,'gquota':{'m':33,'f':25}},
    'NSC': {'building': 'Northside Apartments', 'studios': nsc_studios, 'otherrooms':nsc_otherrooms}, #no gquota?
    'RID': {'building': 'Ridge House', 'cap': 38,'gquota':{'m':19,'f':19}},
    'ROC': {'building': 'Rochdale Village','partialcap':roccap, 'poss_share':[]}, #no gquota? no rooms can be shared...
    'SHE': {'building': 'Sherman Hall', 'cap': 40,'gquota':{'m':14,'f':26}},
    'STB': {'building': 'Stebbins Hall', 'cap': 64,'gquota':{'m':37,'f':27}},
    'WAR': {'building': 'Oscar Wilde House', 'cap': 38,'gquota':{'m':19,'f':19}},
    'WOL': {'building': 'Wolf House', 'cap': 27,'gquota':{'m':14,'f':13}},
    'CNCRB':{'building':'Cancellations Room&Board'},
    'CNCO': {'building': 'Cancellations Other'},
    'CNC0': {'building': 'Cancellations Other'}}

#--------------------------------------
# KYLE AND BETSY, YOU DONT HAVE TO EDIT
#      ANYTHING BELOW HERE
#--------------------------------------

houseinfo['ATH']= houseinfo['PRO'] #just to adjust for Afro being ATH sometimes and PRO othertimes...
houseinfo['WIL']= houseinfo['WAR']

cnt=0
for i,itm in fencap.items():
    cnt+=itm

houseinfo['FEN']['cap']=cnt

cnt=0
for i,itm in roccap.items():
    cnt+=itm

houseinfo['ROC']['cap']=cnt

import os
import csv
import time

mult_list = "RMSlist.csv"
exptlist = "Prettylist.csv"

mult_listP1 = "RMSfulllistP1"
mult_listP2 = "RMSfulllistP2"
mult_listP12 = "RMSfulllistP12"
exceptionlist = ['HIP', 'FEN', 'ROC', 'NSC']

class FullHouse(object):
    """
    Class that implements all methods for Full House List modification
    """
    def __init__(self,in_nom=mult_list,COrun=True):
        """
        Args:
            in_nom : name of file to read in
            COrun : is script being run at CO (changes how loading/saving happens)
        """
        self.in_nom=in_nom
        self.COrun=COrun
        self.tmpinitial={}
        self.initialdict={}
        self.cancellist={}
        self.errorlist=[]
        self.outputcommentlist=[]
    def loadfile(self):
        tmpmultstuff = [] #this is just for loading initial rows
        if self.COrun:
            if not os.path.exists("C:\\"+str(self.in_nom)):
                print("CSV List Input file does not exist! Put it in C folder and name it "+str(self.in_nom))
                self.errorlist.append("CSV List Imput file does not exist! Put it in C folder and name it "+str(self.in_nom))
            else:
                with open('C:\\'+str(self.in_nom)) as csvfile:
                    s1=csv.reader(csvfile,delimiter=',')
                    for blip in s1:
                        tmpmultstuff.append(blip)
        else:
            with open(str(self.in_nom)) as csvfile:
                s1 = csv.reader(csvfile, delimiter=',')
                for blip in s1:
                    tmpmultstuff.append(blip)
        keylist = tmpmultstuff[0]
        Pretmpinitial = {} #keys are application numbers, entries are list of all row entries with that app num, as a dictionary
        for i in range(1, len(tmpmultstuff)):
            nowinput={}
            for k in range(len(keylist)):
                nowinput[keylist[k]] = tmpmultstuff[i][k]
            appnum=nowinput['BSC Application Number']
            if appnum not in Pretmpinitial.keys():
                Pretmpinitial[appnum]=[]
            Pretmpinitial[appnum].append(nowinput)
        if 'Term' in keylist: #this is how I know it is summer (if "Term" column exists)
            self.sumflag=True
            tmpinitial = {mult_listP1:{},mult_listP2:{},mult_listP12:{}}
            #keys for here are the different semester names, keys for this dictionary are row numbers from input list
            cntlis={'1':0,'2':0,'12':0}
            for i in Pretmpinitial.keys():
                flaglis={'1':0,'2':0,'house_p1':None,'house_p2':None,'diff_places_flag':False}
                for j in Pretmpinitial[i]:
                    if 'Summer Period 1' in j['Term']:
                        flaglis['1']+=1
                        if not flaglis['house_p1']:
                            flaglis['house_p1'] = j
                        elif flaglis['house_p1']['Building'] != j['Building']:
                            self.errorlist.append('WARNING. App # '+str(i)+
                                                  ' had multiple bookings for period 1...please look into issue..')
                    if 'Summer Period 2' in j['Term']: #if you move out before per2starts then considered in period 2
                        flaglis['2']+=1
                        if not flaglis['house_p2']:
                            flaglis['house_p2'] = j
                        elif flaglis['house_p2']['Building'] != j['Building']:
                            self.errorlist.append('WARNING. App # '+str(i)+
                                                  ' had multiple bookings for period 2...please look into issue..')
                #Now will put in first entry of Pretmpinitial as if it was a row in the Period1/2/12 files
                if flaglis['house_p1'] and flaglis['house_p2']: #to account for when bookings exist for different houses in summer
                    if flaglis['house_p1']['Building'] != flaglis['house_p2']['Building']:
                        flaglis['diff_places_flag'] = True
                        # print('GOT SOMEONE WHO WAS A DOUBLE DIPPER IN DIFF SEMESTERS: '+str(i))
                if (flaglis['1'] and flaglis['2']) and (not flaglis['diff_places_flag']):
                    cntlis['12']+=1
                    tmpinitial[mult_listP12][cntlis['12']]=flaglis['house_p1']
                else:
                    if flaglis['1']:
                        cntlis['1']+=1
                        tmpinitial[mult_listP1][cntlis['1']]=flaglis['house_p1']
                    if flaglis['2']:
                        cntlis['2']+=1
                        tmpinitial[mult_listP2][cntlis['2']]=flaglis['house_p2']
        else:
            self.sumflag=False
            tmpinitial=Pretmpinitial
        self.tmpinitial=tmpinitial
        return
    def parsefile(self):
        if self.sumflag:
            initialdict = {mult_listP1:{},mult_listP2:{},mult_listP12:{}}  #keys for each dictionary are the house names
            cancellist = {'other': {}, 'R&B': {},'WillMoveIn':{},'Replaced':{}}
            for i in [mult_listP1,mult_listP12,mult_listP2]: #compile initialdict
                for j, vals in self.tmpinitial[i].items():
                    abbrv = vals['Bed Space'].split('-')[0]
                    if abbrv=='CNC':
                        abbrv+=vals['Bed Space'].split('-')[1]
                    housenom = houseinfo[abbrv]['building']
                    out, tmp = self.getentry(vals,abbrv)
                    if 'Cancellations Other' in housenom: #if cancellation then we dont want it
                        if tmp[3] in cancellist['other'].keys():
                            cntr=0
                            flag=1
                            while flag:
                                nom=tmp[3]
                                cntr+=1
                                nom+=str(cntr)
                                if nom not in cancellist['other'].keys():
                                    tmp[3]=nom
                                    flag=0
                        cancellist['other'][tmp[3]] = tmp
                        continue
                    elif 'Cancellations Room&Board' in housenom:
                        if tmp[3] in cancellist['R&B'].keys():
                            cntr=0
                            flag=1
                            while flag:
                                nom=tmp[3]
                                cntr+=1
                                nom+=str(cntr)
                                if nom not in cancellist['R&B'].keys():
                                    tmp[3]=nom
                                    flag=0
                        cancellist['R&B'][tmp[3]] = tmp
                        continue
                    if housenom not in initialdict[i].keys():
                        initialdict[i][housenom]={}
                    if len(out) == 1:
                        if out[0] in initialdict[i][housenom].keys():
                            self.outputcommentlist.append('WARNING! Name '+str(out[0])+' was already in the houselist...'
                                                          'this is probably causing an error.')
                        initialdict[i][housenom][out[0]] = tmp  #key is last name
                    elif len(out)==3: #shared room exception in HiP
                        if 'SHAREDROOM' not in initialdict[i][housenom]['lgs'].keys():
                            initialdict[i][housenom]['lgs']['SHAREDROOM'] = []
                        tmp[1]=1
                        initialdict[i][housenom]['lgs']['SHAREDROOM'].append(tmp) #this could be more than one pair
                    else:
                        if out[0] not in initialdict[i][housenom].keys():
                            initialdict[i][housenom][out[0]] = {}
                        initialdict[i][housenom][out[0]][out[1]] = tmp
                    if housenom in ['Fenwick Weavers Village','Rochdale Village']:
                        for k in houseinfo[abbrv]['partialcap'].keys():
                            if abbrv=='FEN':
                                rmkey=float(k)
                            else:
                                rmkey=str(k)
                            if rmkey not in initialdict[i][housenom].keys():
                                initialdict[i][housenom][rmkey]={}
                    elif housenom=='Northside Apartments':
                        for typerm in ['studios','otherrooms']:
                            for k in houseinfo['NSC'][typerm]:
                                if float(k) not in initialdict[i][housenom].keys():
                                    initialdict[i][housenom][float(k)]={}
            self.initialdict=initialdict
            self.cancellist=cancellist
            return
        else:
            initialdict = {}  #keys for this dictionary are the house names
            cancellist = {'other': {}, 'R&B': {},'WillMoveIn':{},'Replaced':{}}
            #go through each row and see if building
            for j, vals in self.tmpinitial.items():
                if len(vals)!=1:
                    tmpkeepers=[]
                    for k in vals:
                        abbrv=k['Bed Space'].split('-')[0]
                        if abbrv=='CNC':
                            abbrv+=k['Bed Space'].split('-')[1]
                        out, tmp = self.getentry(k,abbrv)
                        if 'CNC' not in k['Bed Space']:
                            tmpkeepers.append([abbrv,k,tmp])
                        else:
                            housenom = houseinfo[abbrv]['building']
                            if 'Cancellations Other' in housenom:
                                cancellist['other'][tmp[3]] = tmp
                            elif 'Cancellations Room&Board' in housenom:
                                cancellist['R&B'][tmp[3]] = tmp
                    tmpkeepers.sort()
                    if len(tmpkeepers)!=1:
                        tmpnoms=[]
                        for k in tmpkeepers:
                            if k[0] not in tmpnoms:
                                tmpnoms.append(k[0])
                        if len(tmpnoms)!=1:
                            self.errorlist.append('found more than 1 entry for '+str(j)+
                                                  ' ('+str(tmpnoms)+') Just using one of them...')
                        else:
                            self.errorlist.append('found more than 1 entry for '+str(j)+
                                                  ' at '+str(tmpnoms[0])+'. Only using one unintelligently '
                                                                         'since trying to avoid use of Move Out data..')
                    vals=tmpkeepers[0][1]
                else:
                    vals=vals[0]
                abbrv = vals['Bed Space'].split('-')[0]
                if abbrv=='CNC':
                    abbrv+=vals['Bed Space'].split('-')[1]
                housenom = houseinfo[abbrv]['building']
                out, tmp = self.getentry(vals,abbrv)
                if 'Cancellations Other' in housenom:
                    cancellist['other'][tmp[3]] = tmp
                    continue
                elif 'Cancellations Room&Board' in housenom:
                    cancellist['R&B'][tmp[3]] = tmp
                    continue
                if housenom not in initialdict.keys():
                    initialdict[housenom]={}
                if len(out) == 1:
                    initialdict[housenom][out[0]] = tmp  #key is last name
                elif len(out)==3: #shared room exception in HiP
                    if 'SHAREDROOM' not in initialdict[housenom]['lgs'].keys():
                        initialdict[housenom]['lgs']['SHAREDROOM'] = []
                    tmp[1]=1
                    initialdict[housenom]['lgs']['SHAREDROOM'].append(tmp) #this could be more than one pair
                else:
                    if out[0] not in initialdict[housenom].keys():
                        initialdict[housenom][out[0]] = {}
                    initialdict[housenom][out[0]][out[1]] = tmp
            #now remove people form cancelation list
            for u in initialdict.keys():
                for abb in houseinfo.keys():
                    if u==houseinfo[abb]['building']:
                        sym=abb.upper()
                if sym not in exceptionlist:
                    for v in initialdict[u].keys():
                        if (v in cancellist['R&B']) or (v in cancellist['other']):
                            del initialdict[u][v]
                elif sym=='HIP':
                    for v in initialdict[u]['lgs'].keys():
                        if v=='SHAREDROOM':
                            dellist=[]
                            for h in initialdict[u]['lgs'][v]:
                                if (h[3] in cancellist['R&B']) or (h[3] in cancellist['other']):
                                    dellist.append(h)
                                else:
                                    continue
                            newshare=[]
                            for h in initialdict[u]['lgs'][v]:
                                if h not in dellist:
                                    newshare.append(h)
                            initialdict[u]['lgs'][v]=newshare
                            if len(initialdict[u]['lgs'][v])==1:
                                initialdict[u]['lgs'][str(newshare[0][3])]=newshare[0]
                                del initialdict[u]['lgs']['SHAREDROOM']
                        else:
                            if (v in cancellist['R&B']) or (v in cancellist['other']):
                                del initialdict[u]['lgs'][v]
                    for v in initialdict[u]['sts'].keys():
                        if (v in cancellist['R&B']) or (v in cancellist['other']):
                            del initialdict[u]['sts'][v]
                elif sym in ['ROC','FEN','NSC']:
                    for v in initialdict[u].keys():
                        for h in initialdict[u][v].keys():
                            if (h in cancellist['R&B']) or (h in cancellist['other']):
                                del initialdict[u][v][h]
            for abbrv in ['FEN','ROC']:
                housenom=houseinfo[abbrv]['building']
                for k in houseinfo[abbrv]['partialcap'].keys():
                    if abbrv=='FEN':
                        rmkey=float(k)
                    else:
                        rmkey=str(k)
                    if rmkey not in initialdict[housenom].keys():
                        initialdict[housenom][k]={}
            housenom='Northside Apartments'
            for typerm in ['studios','otherrooms']:
                for k in houseinfo['NSC'][typerm]:
                    if float(k) not in initialdict[housenom].keys():
                        initialdict[housenom][float(k)]={}
            self.initialdict=initialdict
            self.cancellist=cancellist
            return
    def getentry(self,indict,nom):
        #nom is the abbreviation name...
        Person_name = str(indict['Last Name']) + ', ' + str(indict['First Name'])
        gndr = indict['Gender Identification']
        if gndr == 'Woman':
            Person_name += ' (f)'
        elif gndr == 'Man':
            Person_name += ' (m)'
        else:
            print("Could not find gender for ", Person_name)
            self.errorlist.append("Could not find gender for " + str(Person_name))
        stat = indict['Contract Status (S MA U)']
        cmt = indict['Comments']
        appnum = indict['BSC Application Number']
        emal = indict['Permanent Email']
        pts = indict['Points']
        tmphere = [stat, Person_name, cmt, appnum, emal, pts]
        bdspc = indict['Bed Space'].split('-')
        if nom.upper() in exceptionlist:
            rtcd = indict['Rate Code'].split('-')
            if nom.upper() == 'FEN':
                tmphere.insert(0, 0)
                tmphere.insert(0, str(nom) + ' ' + str(bdspc[1]))
                out = [float(bdspc[1]), Person_name]
            elif nom.upper() == 'ROC':
                if len(bdspc) != 3:  #THEN THIS IS STUDIO
                    tmphere.insert(0, 0)
                    tmphere.insert(0, str(nom) + ' ' + str(bdspc[1][:-1]))
                    out = [bdspc[1][:-1], Person_name]
                else:
                    tmphere.insert(0, 0)
                    tmphere.insert(0, str(nom) + ' ' + str(bdspc[1]))
                    out = [bdspc[1], Person_name]
            elif nom.upper() == 'NSC':
                if len(bdspc) != 3:  #THEN THIS IS STUDIO
                    tmphere.insert(0, 0)
                    tmphere.insert(0, str(nom) + ' ' + bdspc[1][:-1])
                    out = [float(bdspc[1][:-1]), Person_name]
                else:
                    tmphere.insert(0, 0)
                    tmphere.insert(0, str(nom) + ' ' + str(bdspc[1]))
                    out = [float(bdspc[1]), Person_name]
            elif nom.upper() == "HIP":
                if len(rtcd) == 3:  #for shared room
                    tmphere.insert(0, str(rtcd[1]) + '.' + str(rtcd[2])) #if
                    out = [Person_name,'RS'] #out will be 3 long if room share
                else:
                    tmphere.insert(0, 0)
                    out = [Person_name]
                if rtcd[1] == 'LGS':
                    tmphere.insert(0, str(nom) + ' lgs')
                    out.insert(0, 'lgs')
                elif rtcd[1] == 'STS':
                    tmphere.insert(0, str(nom) + ' sts')
                    out.insert(0, 'sts')
            else:
                print(tmphere)
                print('Could not find lgs/sts for HIP member', Person_name)
                self.errorlist.append('Could not find lgs/sts for HIP member ' + str(Person_name))
        else:
            out = [Person_name]
            tmphere.insert(0, bdspc[1])
            tmphere.insert(0, nom)
        return out, tmphere
    def getabbrv(self,nom):
        for abb in houseinfo.keys():
            if nom==houseinfo[abb]['building']:
                sym=abb.upper()
        return sym
    def getgender(self,row):
        if '(f)' in row[3]:
            return 'f'
        else:
            return 'm'
    def getfinaldict(self):
        finaldict = {} #dictionary with house name and array that follows for exporting to list quickly
        if self.sumflag:
            for j in [mult_listP1,mult_listP2,mult_listP12]:
                for i in self.initialdict[j].keys():
                    finaldict[i] = {}
            for j in [mult_listP1,mult_listP2,mult_listP12]:
                for i in finaldict.keys(): #make sure all lists have all houses as keys...
                    if i not in self.initialdict[j].keys():
                        self.initialdict[j][i]={}
            for i in finaldict.keys(): #will do each house all at once (assuming all houses in mult_listP1...)
                # self.outputcommentlist.append('\n')
                finlist=[]
                vacnamelistp1=[] #for summary of rooms with vacancies; note this only used for exception list?
                vacnamelistp2=[] #for summary of rooms with vacancies
                abbrv=self.getabbrv(i)
                if abbrv not in exceptionlist:
                    noms12=self.initialdict[mult_listP12][i].keys()
                    noms1=self.initialdict[mult_listP1][i].keys()
                    noms2=self.initialdict[mult_listP2][i].keys()
                    noms12.sort() #alphabetical
                    noms1.sort()
                    noms2.sort()
                    finaldict[i]['Per1currcap']=len(noms12)+len(noms1)
                    finaldict[i]['Per2currcap']=len(noms2)+len(noms12)
                    finaldict[i]['Per1vacs']=int(houseinfo[abbrv]['cap'])-int(finaldict[i]['Per1currcap'])
                    finaldict[i]['Per2vacs']=int(houseinfo[abbrv]['cap'])-int(finaldict[i]['Per2currcap'])
                    if finaldict[i]['Per1vacs']<0:
                        self.errorlist.append(str(i)+' has '+str(-finaldict[i]['Per1vacs'])+
                                            ' more people than it should have in Period 1. '
                                            'Check the capacity assignments at top of script')
                    elif finaldict[i]['Per1vacs']>0:
                        self.outputcommentlist.append('Found '+str(finaldict[i]['Per1vacs'])+
                                                      ' vacancies at '+str(i)+' in Period 1')
                    if finaldict[i]['Per2vacs']<0:
                        self.errorlist.append(str(i)+' has '+str(-finaldict[i]['Per2vacs'])+
                                              ' more people than it should have in Period 2.'
                                              ' Check the capacity assignments at top of Broberg HL script')
                    elif finaldict[i]['Per2vacs']>0:
                        self.outputcommentlist.append('Found '+str(finaldict[i]['Per2vacs'])+
                                                      ' vacancies at '+str(i)+' in Period 2')
                    justp2={'m':[],'f':[]}
                    for j in noms2:
                        if '(f)' in j:
                            justp2['f'].append(j)
                        else:
                            justp2['m'].append(j)
                    justp2['f'].sort()
                    justp2['m'].sort()
                    #now start the finlist with P12 people, followed by P1 people
                    cnt=0
                    gender_cntr={1:{'m':0,'f':0},2:{'m':0,'f':0}}
                    vac_cntr={1:{'m':0,'f':0},2:{'m':0,'f':0}}
                    for j in noms12:
                        cnt+=1
                        tmp1=self.initialdict[mult_listP12][i][j][:]
                        tmp1[1]=cnt
                        tmp1.append('')
                        tmp1.append('(same)')
                        finlist.append(tmp1)
                        gndr = self.getgender(tmp1)
                        gender_cntr[1][gndr]+=1
                        gender_cntr[2][gndr]+=1
                    for j in noms1:
                        cnt+=1
                        tmp1=self.initialdict[mult_listP1][i][j][:]
                        gndr = self.getgender(tmp1)
                        tmp1[1]=cnt
                        gender_cntr[1][gndr]+=1
                        if len(justp2[gndr])!=0:
                            tmp2=self.initialdict[mult_listP2][i][justp2[gndr][0]][:]
                            del tmp2[0]
                            del tmp2[0]
                            for k in tmp2:
                                tmp1.append(k)
                            del justp2[gndr][0]#remove the name so you don't use it again
                            gender_cntr[2][gndr]+=1
                        else:
                            tmp1.append('')
                            vac_cntr[2][gndr]+=1
                            if gndr=='m':
                                tmp1.append('P2 Male Vacancy')
                            else:
                                tmp1.append('P2 Female Vacancy')
                        finlist.append(tmp1)
                    for j in justp2['m']: #this part might be less essential in the grand scheme of the code..
                        # ...because wont have P2 assignments before P12/P1 assignments
                        cnt+=1
                        tmp2=self.initialdict[mult_listP2][i][j][:]
                        tmp1=[tmp2.pop(0),cnt]
                        del tmp2[0]
                        tmp1.append('P1 Male Vacancy')
                        gender_cntr[2]['m']+=1
                        vac_cntr[1]['m']+=1
                        for k in range(5):
                            tmp1.append('')
                        for k in tmp2:
                            tmp1.append(k)
                        finlist.append(tmp1)
                    for j in justp2['f']:
                        cnt+=1
                        tmp2=self.initialdict[mult_listP2][i][j][:]
                        tmp1=[tmp2.pop(0),cnt]
                        del tmp2[0]
                        tmp1.append('P1 Female Vacancy')
                        gender_cntr[2]['f']+=1
                        vac_cntr[1]['f']+=1
                        for k in range(5):
                            tmp1.append('')
                        for k in tmp2:
                            tmp1.append(k)
                        finlist.append(tmp1)
                    #This part corrects for errors in gender variations that may occur between periods...specifically,
                    #allow for males to be in female rooms if needed...
                    if (cnt > houseinfo[abbrv]['cap']) and ((vac_cntr[1]['m'] and vac_cntr[2]['f'])
                                                            or (vac_cntr[1]['f'] and vac_cntr[2]['m'])):
                        self.outputcommentlist.append(str(abbrv)+
                                                      ' house had an inbalance of genders between periods.'
                                                      ' Mixed some gendered rooms in order to avoid increasing '
                                                      'house capacities...')
                        while (cnt > houseinfo[abbrv]['cap']):
                            tmpgendervacs = {1:{'m':[],'f':[]},2:{'m':[],'f':[]}} #for storing room nums
                            for icnt in range(cnt):
                                row = finlist[icnt]
                                if 'VACANCY' in row[2].upper():
                                    if 'FEMALE' in row[2].upper():
                                        tmpgendervacs[1]['f'].append(icnt)
                                    else:
                                        tmpgendervacs[1]['m'].append(icnt)
                                elif 'VACANCY' in row[9].upper():
                                    if 'FEMALE' in row[9].upper():
                                        tmpgendervacs[2]['f'].append(icnt)
                                    else:
                                        tmpgendervacs[2]['m'].append(icnt)
                            for per in [1,2]:
                                for g in ['m','f']:
                                    tmpgendervacs[per][g].sort(reverse=True)
                            if len(tmpgendervacs[1]['m']) > len(tmpgendervacs[2]['f']):
                                pulloutnum = tmpgendervacs[2]['f'].pop(0) #this non vacant period in this row will be moved to male vacancy
                                movetonum = tmpgendervacs[1]['m'].pop(0)
                                vac_cntr[2]['f']-=1
                                vac_cntr[1]['m']-=1
                                semmove = 1
                            elif len(tmpgendervacs[2]['m']) > len(tmpgendervacs[1]['f']):
                                pulloutnum = tmpgendervacs[1]['f'].pop(0) #this non vacant period in this row will be moved to male vacancy
                                movetonum = tmpgendervacs[2]['m'].pop(0)
                                vac_cntr[1]['f']-=1
                                vac_cntr[2]['m']-=1
                                semmove = 2
                            elif (len(tmpgendervacs[1]['f']) >= len(tmpgendervacs[2]['m'])) and \
                                    (len(tmpgendervacs[1]['f']) and len(tmpgendervacs[2]['m'])): #made equality on purpose here
                                pulloutnum = tmpgendervacs[2]['m'].pop(0) #this non vacant period in this row will be moved to female vacancy
                                movetonum = tmpgendervacs[1]['f'].pop(0)
                                vac_cntr[2]['m']-=1
                                vac_cntr[1]['f']-=1
                                semmove = 1
                            elif len(tmpgendervacs[2]['f']) >= len(tmpgendervacs[1]['m']) and \
                                    (len(tmpgendervacs[2]['f']) and len(tmpgendervacs[1]['m'])):  #made equality on purpose here
                                pulloutnum = tmpgendervacs[1]['m'].pop(0) #this non vacant period in this row will be moved to male vacancy
                                movetonum = tmpgendervacs[2]['f'].pop(0)
                                vac_cntr[1]['m']-=1
                                vac_cntr[2]['f']-=1
                                semmove = 2
                            if semmove==1:
                                for val in range(0,8):
                                    finlist[movetonum][val] = finlist[pulloutnum][val]
                            elif semmove==2:
                                for val in range(8,len(finlist[pulloutnum])):
                                    try:
                                        finlist[movetonum][val] = finlist[pulloutnum][val]
                                    except:
                                        finlist[movetonum].append(finlist[pulloutnum][val])
                            cnt-=1
                            del finlist[pulloutnum]
                    full_vacs = int(houseinfo[abbrv]['cap']) - len(finlist) #count number of full vacancies left
                    mal_vacs = houseinfo[abbrv]['gquota']['m']-max(gender_cntr[1]['m'],gender_cntr[2]['m'])
                    fem_vacs = houseinfo[abbrv]['gquota']['f']-max(gender_cntr[1]['f'],gender_cntr[2]['f'])
                    hausnom=finlist[-1][0]
                    if full_vacs>0:
                        while full_vacs>0:
                            cnt+=1
                            if mal_vacs > 0:
                                finlist.append([hausnom,cnt,'Full Summer Male Vacancy'])
                                mal_vacs-=1
                                full_vacs-=1
                                vac_cntr[1]['m']+=1
                                vac_cntr[2]['m']+=1
                            elif fem_vacs > 0:
                                finlist.append([hausnom,cnt,'Full Summer Female Vacancy'])
                                fem_vacs-=1
                                full_vacs-=1
                                vac_cntr[1]['f']+=1
                                vac_cntr[2]['f']+=1
                    finlist.append(['','','','','','','',''])
                    title=str(i)+' has a capacity of '+str(houseinfo[abbrv]['cap'])+'.'
                    mleftp1 = vac_cntr[1]['m']
                    mleftp2 = vac_cntr[2]['m']
                    fleftp1 = vac_cntr[1]['f']
                    fleftp2 = vac_cntr[2]['f']
                    if mleftp1 or mleftp2 or fleftp1 or fleftp2:
                        title+=' Vacancies exist = P1: (male: '+str(mleftp1)+', female: '+str(fleftp1)+'),' \
                                                        ' P2: (male: '+str(mleftp2)+', female: '+str(fleftp2)+').'
                    else:
                        title+=' No Vacancies.'
                    finlist.insert(0,[title])
                    finaldict[i]['output']=finlist
                    for per in [1,2]:
                        for g in ['male','female']:
                            gdiff = houseinfo[abbrv]['gquota'][g[0]] - gender_cntr[per][g[0]] #just using first letter as key
                            if gdiff < 0:
                                self.errorlist.append('At '+str(i)+' in period '+str(per)+
                                                              ' you have exceeded '+str(g)+' quota by '+str(-gdiff))
                else: #exceptions from here on
                    if abbrv in ['FEN','ROC']:
                        def makeroom(numstr):
                            rmout=[]
                            cnt=0
                            try:  #different types of keys
                                innum=int(numstr)
                            except:
                                innum=numstr
                            try:
                                keylisP1=self.initialdict[mult_listP1][i][innum].keys()
                            except:
                                keylisP1=[]
                            try:
                                keylisP2=self.initialdict[mult_listP2][i][innum].keys()
                            except:
                                keylisP2=[]
                            try:
                                keylisP12=self.initialdict[mult_listP12][i][innum].keys()
                            except:
                                keylisP12=[]
                            keylisP1.sort()
                            keylisP2.sort()
                            keylisP12.sort()
                            vacp1=0 #enforcing gender here isnt possible because ratio not enforced for indiviudal rooms
                            vacp2=0
                            for j in keylisP12:
                                cnt+=1
                                out=self.initialdict[mult_listP12][i][innum][j]
                                out[1]=cnt
                                out.append('')
                                out.append('(same)')
                                rmout.append(out)
                            for j in keylisP1: #now append session 1 people to room if slot is free
                                cnt+=1
                                out=self.initialdict[mult_listP1][i][innum][j]
                                out[1]=cnt
                                if len(keylisP2):
                                    tmpout=self.initialdict[mult_listP2][i][innum][keylisP2[0]]
                                    del tmpout[0]
                                    del tmpout[0]
                                    for k in tmpout:
                                        out.append(k)
                                    del keylisP2[0]
                                else:
                                    out.append('')
                                    out.append('P2 Vacancy')
                                    vacp2+=1
                                rmout.append(out)
                            for j in keylisP2:
                                cnt+=1
                                tmp=self.initialdict[mult_listP2][i][innum][j]
                                del tmp[0]
                                out=[str(abbrv)+' '+str(numstr),cnt,'P1 Vacancy','','','','','']
                                vacp1+=1
                                for k in tmp:
                                    out.append(k)
                                rmout.append(out)
                            partcap=houseinfo[abbrv]['partialcap'][numstr]
                            if partcap<cnt:
                                if numstr in houseinfo[abbrv]['poss_share']:
                                    partcap=2 #make it a shared room...
                                    if partcap>=cnt:
                                        #print('In '+str(i)+' making room '+str(innum)+' a shared room.')
                                        self.outputcommentlist.append('In '+str(i)+' making room '+str(innum)+' a shared room.')
                                        for k in rmout:
                                            k[0]+='*'
                                    else:
                                        #print('In '+str(i)+' room '+str(innum)+' has too many people.')
                                        self.outputcommentlist.append('In '+str(i)+' room '+str(innum)+
                                                                      ' has too many people (it can be shared, but only by two people).')
                                        for k in rmout:
                                            k[0]+='(Error)'
                                else:
                                    #print('In '+str(i)+' room '+str(innum)+' has too many people.')
                                    self.outputcommentlist.append('In '+str(i)+' room '+str(innum)+' has too many people.')
                                    for k in rmout:
                                        k[0]+='(Error)'
                            else:
                                fullvacs=partcap-cnt
                                for k in range(fullvacs):
                                    cnt+=1
                                    vacp1+=1
                                    vacp2+=1
                                    rmout.append([abbrv+' '+str(numstr),cnt,'FULLY VACANT','','','','','','',''])
                            rmout.append(['','','','','','','',''])
                            return vacp1,vacp2,rmout
                        rmnums=houseinfo[abbrv]['partialcap'].keys()
                        rmnums.sort() #sorts in right order for either house
                        totvacp1=0 #is gender something we want to enforce?
                        vacp1str='(room '
                        totvacp2=0
                        vacp2str='(room '
                        for u in rmnums:
                            vcs1,vcs2,ot=makeroom(u)
                            if vcs1:
                                totvacp1+=vcs1
                                vacp1str+=u+' '
                            if vcs2:
                                totvacp2+=vcs2
                                vacp2str+=u+' '
                            for v in ot:
                                finlist.append(v)
                        if vacp1str!='(room ':
                            vacp1str=vacp1str[:-1]+')'
                        else:
                            vacp1str=''
                        if vacp2str!='(room ':
                            vacp2str=vacp2str[:-1]+')'
                        else:
                            vacp2str=''
                        finaldict[i]['Per1vacs']=str(totvacp1)+' '+vacp1str
                        finaldict[i]['Per2vacs']=str(totvacp2)+' '+vacp2str
                    elif abbrv=='NSC':
                        def makeroom(numstr):
                            rmout=[]
                            cnt=0
                            keylis=[]
                            keylis2=[]
                            if numstr in self.initialdict[mult_listP1][i].keys():
                                for j in self.initialdict[mult_listP1][i][numstr].keys():
                                    keylis.append(j)
                            if numstr in self.initialdict[mult_listP12][i].keys():
                                for j in self.initialdict[mult_listP12][i][numstr].keys():
                                    keylis.append(j)
                            if numstr in self.initialdict[mult_listP2][i].keys():
                                for j in self.initialdict[mult_listP2][i][numstr].keys():
                                    keylis2.append(j)
                            keylis.sort()
                            keylis2.sort()
                            vacp1=0 #enforcing gender here isnt possible because ratio not enforced for indiviudal rooms
                            vacp2=0
                            for j in keylis:
                                cnt+=1
                                if (numstr in self.initialdict[mult_listP12][i].keys()) and \
                                        (j in self.initialdict[mult_listP12][i][numstr].keys()):
                                    perkey = mult_listP12
                                else:
                                    perkey = mult_listP1
                                out=self.initialdict[perkey][i][numstr][j]
                                if perkey==mult_listP12:
                                    #keylis2.remove(j)
                                    for k in range(6):
                                        if k==1:
                                            out.append('(same)')
                                        else:
                                            out.append('')
                                out[1]=cnt
                                rmout.append(out)
                            for j in keylis2: #now append session 2 people to room if slot if free
                                out=self.initialdict[mult_listP2][i][numstr][j]
                                del out[0]
                                del out[0]
                                for k in rmout:
                                    if len(k)==8: #other wise room is full both semesters...
                                        for u in out:
                                            k.append(u)
                                        keylis2.remove(j)
                                        break
                            for j in keylis2: #if this still exists then no one exists for them in previous period
                                cnt+=1
                                out=self.initialdict[mult_listP2][i][numstr][j]
                                del out[0]
                                hsnm=out.pop(0)
                                for k in range(5):
                                    out.insert(0,'')
                                out.insert(0,'P1 VACANCY')
                                out.insert(0,cnt)
                                out.insert(0,hsnm)
                                vacp1+=1
                                rmout.append(out)
                            for j in rmout: #search for any vacant spots in period 2
                                if len(j)==8:
                                    vacp2+=1
                                    for k in range(6):
                                        if k==1:
                                            j.append('P2 Vacancy')
                                        else:
                                            j.append('')
                            if cnt>1 and numstr in nsc_studios:
                                #print('   Room '+str(numstr)+' at NSC is a studio but has '+str(cnt)+' people.')
                                self.errorlist.append('Room '+str(numstr)+
                                                      ' at NSC is a studio but has '+str(cnt)+' people.')
                                for v in rmout:
                                    v[0]='(bad)'+str(v[0])
                            if cnt==0: #only introduce one vacancy if no booked yet for summer (NSC)
                                vacp1+=1
                                vacp2+=1
                                cnt+=1
                                rmout.append(['NSC '+str(numstr),cnt,'FULLY VACANT','','','','','','',''])
                            if cnt>2:
                                #print('   (ERROR!) Room '+str(numstr)+' has '+str(vacp1)+' vacancies?')
                                self.outputcommentlist.append('(ERROR) In Northside, Room '
                                                              +str(numstr)+' has '+str(vacp1)+' vacancies?')
                                for v in rmout:
                                    v[0]='(bad?)'+str(v[0])
                            if vacp1: #for listing if vacancies exist
                                #print('   Room '+str(numstr)+' has '+str(vacp1)+' vacancies in period1')
                                self.outputcommentlist.append('In Northside, Room '+str(numstr)+
                                                              ' has '+str(vacp1)+' vacancies in Period 1')
                                vacnamelistp1.append([numstr,vacp1])
                            if vacp2:
                                #print('   Room '+str(numstr)+' has '+str(vacp2)+' vacancies in period2')
                                self.outputcommentlist.append('In Northside, Room '+str(numstr)+' has '
                                                              +str(vacp2)+' vacancies in Period 2')
                                vacnamelistp2.append([numstr,vacp2])
                            rmout.append(['','','','','','','',''])
                            return vacp1,vacp2,cnt,rmout
                        totvacp1=0
                        vacp1str='(room '
                        totvacp2=0
                        vacp2str='(room '
                        cap=0
                        rmnums=list(set(nsc_studios) | set(nsc_otherrooms))
                        rmnums.sort()
                        for u in rmnums:
                            vcs1,vcs2,cnt,ot=makeroom(u)
                            if vcs1:
                                totvacp1+=vcs1
                                vacp1str+=str(u)+' '
                            if vcs2:
                                totvacp2+=vcs2
                                vacp2str+=str(u)+' '
                            cap+=cnt
                            for v in ot:
                                finlist.append(v)
                        if vacp1str!='(room ':
                            vacp1str=vacp1str[:-1]+')'
                        else:
                            vacp1str=''
                        if vacp2str!='(room ':
                            vacp2str=vacp2str[:-1]+')'
                        else:
                            vacp2str=''
                        houseinfo[abbrv]['cap']=cap
                        finaldict[i]['Per1vacs']=str(totvacp1)+' '+vacp1str
                        finaldict[i]['Per2vacs']=str(totvacp2)+' '+vacp2str
                    elif abbrv=='HIP':  #working on this on 4/2/16. Have P1 and P12 in stsnoms
                        stsnoms=[]
                        stsnoms2=[]
                        lgsnoms=[]
                        lgsnoms2=[]
                        for rmtype in ['sts','lgs']:
                            for sem in [mult_listP1,mult_listP2,mult_listP12]:
                                if rmtype in self.initialdict[sem][i].keys():
                                    for j in self.initialdict[sem][i][rmtype].keys():
                                        if sem is not mult_listP2:
                                            if rmtype=='sts':
                                                stsnoms.append(j)
                                            else:
                                                lgsnoms.append(j)
                                        else:
                                            if rmtype=='sts':
                                                stsnoms2.append(j)
                                            else:
                                                lgsnoms2.append(j)
                        stsnoms.sort() #alphabetical
                        stsnoms2.sort()
                        lgsnoms.sort()
                        lgsnoms2.sort()
                        p1totvac={'sts':0,'lgs':0}
                        p2totvac={'sts':0,'lgs':0}
                        if 'SHAREDROOM' in lgsnoms:
                            cnt=1
                            tmpcnt=0
                            if 'SHAREDROOM' in self.initialdict[mult_listP12][i]['lgs'].keys():
                                perkey = mult_listP12
                            else:
                                perkey = mult_listP1
                            for j in self.initialdict[perkey][i]['lgs']['SHAREDROOM']:
                                tmpcnt+=1 #for changing room number if multi shared rooms exist
                                if (1+(tmpcnt-1.)/2.)==cnt+1:
                                    cnt+=1
                                j[0]='*'+j[0]
                                j[1]=cnt
                                finlist.append(j)
                            if 'SHAREDROOM' in lgsnoms2:
                                if self.initialdict[mult_listP2][i]['lgs']['SHAREDROOM']==self.initialdict[perkey][i]['lgs']['SHAREDROOM']:
                                    for j in finlist:
                                        j.append('')
                                        j.append('(same)')
                                elif len(self.initialdict[mult_listP2][i]['lgs']['SHAREDROOM']): #different people sharing rooms, but same amount exists...
                                    for j in range(len(self.initialdict[mult_listP2][i]['lgs']['SHAREDROOM'])):
                                        del self.initialdict[mult_listP2][i]['lgs']['SHAREDROOM'][j][0]
                                        del self.initialdict[mult_listP2][i]['lgs']['SHAREDROOM'][j][0]
                                        for k in self.initialdict[mult_listP2][i]['lgs']['SHAREDROOM'][j]:
                                            tmp=finlist[j][:]
                                            for u in k:
                                                tmp.append(u)
                                else: #THIS is weird case where there aren't the same number of people in period 2 who are sharing...
                                    self.errorlist.append('FATAL ERROR - detected decrease in '
                                                          'number of people involved in shared rooms at HIP house'
                                                          ' from period 1 to period 2. Script breaks when this happens')
                                    sharedp1size = len(self.initialdict[perkey][i]['lgs']['SHAREDROOM'])
                                    sharedp2size = len(self.initialdict[mult_listP2][i]['lgs']['SHAREDROOM'])
                                    """
                                    TODO: @thispart FIGURE OUT SOME WRAP AROUND THING FOR IF SHARED ROOMS ARE DIFFERENT SIZES...
                                    """
                            elif perkey==mult_listP12:
                                for j in finlist:
                                        j.append('')
                                        j.append('(same)')
                            else:
                                tmp=self.initialdict[mult_listP2][i]['lgs'][lgsnoms2[0]][:]
                                del tmp[0]
                                del tmp[0]
                                for u in tmp:
                                    finlist[1].append(u)
                                lgsnoms2.remove(lgsnoms2[0])
                            lgsnoms.remove('SHAREDROOM')
                        elif 'SHAREDROOM' in lgsnoms2:
                            cnt=1
                            if lgsnoms[0] in self.initialdict[mult_listP12][i]['lgs'].keys():
                                perkey = mult_listP12
                            else:
                                perkey = mult_listP1
                            tmp=self.initialdict[perkey][i]['lgs'][lgsnoms[0]]
                            tmp[0]='*'+str(tmp[0])
                            tmp[1]=cnt
                            tmp1=self.initialdict[mult_listP2][i]['lgs']['SHAREDROOM'][:]
                            for u in tmp1:
                                del u[0]
                                del u[0]
                            for u in tmp1[0]:
                                tmp.append(u)
                            finlist.append(tmp)
                            tmp=['*HIP lgs',cnt,'','','','','','']
                            del tmp1[0]
                            for u in tmp1:
                                tmp2=tmp[:]
                                for v in u:
                                    tmp2.append(v)
                                finlist[1].append(tmp2)
                            lgsnoms.remove(lgsnoms[0])
                            lgsnoms2.remove('SHAREDROOM')
                        else: #no shared rooms
                            cnt=0
                        #do deluxes past shared rooms
                        stufftoremove=[]
                        stufftoremove2=[]
                        for j in lgsnoms:
                            cnt+=1
                            if j in self.initialdict[mult_listP12][i]['lgs'].keys():
                                perkey = mult_listP12
                            else:
                                perkey = mult_listP1
                            stufftoremove.append(j)
                            tmp=self.initialdict[perkey][i]['lgs'][j]
                            tmp[1]=cnt
                            if perkey == mult_listP12:
                                stufftoremove2.append(j)
                                tmp.append('')
                                tmp.append('(same)')
                            finlist.append(tmp)
                        for j in stufftoremove:
                            lgsnoms.remove(j)
                        for j in finlist:
                            if len(j)==8:
                                if len(lgsnoms2)==0:
                                    j.append('')
                                    j.append('P2 vacancy')
                                    p2totvac['lgs']+=1
                                else:
                                    tmp=lgsnoms2[0]
                                    tmp1=self.initialdict[mult_listP2][i]['lgs'][tmp]
                                    del tmp1[0]
                                    del tmp1[0]
                                    for u in tmp1:
                                        j.append(u)
                                    lgsnoms2.remove(tmp)
                        for j in lgsnoms2: #add additional names...
                            cnt+=1
                            p1totvac['lgs']+=1
                            tmp=['HIP lgs',cnt,'P1 Vacant','','','','','']
                            tmp1=self.initialdict[mult_listP2][i]['lgs'][j][:]
                            del tmp1[0]
                            del tmp1[0]
                            for u in tmp1:
                                tmp.append(u)
                            finlist.append(tmp)
                        vaclgs=houseinfo[abbrv]['partialcap']['lgs']-cnt
                        if vaclgs>0:
                            for j in range(vaclgs):
                                cnt+=1
                                tmp=['HIP lgs',cnt,'FULLY VACANT','','','','','','','']
                                p1totvac['lgs']+=1
                                p2totvac['lgs']+=1
                                finlist.append(tmp)
                        elif vaclgs<0:
                            #print('   (ERROR!) HIP lgs has negative vacancies?')
                            self.outputcommentlist.append('(ERROR) HIP lgs has negative vacancies? '
                                                     'Change partialcap listing at top of script'
                                                     ' to fix this issue (rooms cnted='+str(cnt)+
                                                     ' and lgs capacity='+str(houseinfo[abbrv]['partialcap']['lgs']))
                        finlist.append(['','','','','','','','','',''])
                        #now do sts
                        cnt=0
                        stufftoremove=[]
                        stufftoremove2=[]
                        stsfinlist=[] #seperate the stsfinlist before adding to finlist...
                        for j in stsnoms:
                            cnt+=1
                            if j in self.initialdict[mult_listP12][i]['sts'].keys():
                                perkey = mult_listP12
                            else:
                                perkey = mult_listP1
                            stufftoremove.append(j)
                            tmp=self.initialdict[perkey][i]['sts'][j]
                            tmp[1]=cnt
                            if perkey == mult_listP12:
                                stufftoremove2.append(j)
                                tmp.append('')
                                tmp.append('(same)')
                            stsfinlist.append(tmp)
                        for j in stufftoremove:
                            stsnoms.remove(j)
                        #now account for stsfinlist vals that have 8 entries...and put stsnoms2 in there...
                        for j in stsfinlist:
                            if len(j)==8:
                                if len(stsnoms2)==0:
                                    j.append('')
                                    j.append('P2 Vacancy')
                                    p2totvac['sts']+=1
                                else:
                                    nom=stsnoms2[0]
                                    tmp=self.initialdict[mult_listP2][i]['sts'][nom]
                                    del tmp[0]
                                    del tmp[0]
                                    stsnoms2.remove(nom)
                                    for u in tmp:
                                        j.append(u)
                        #now account for left over stsnoms2 (so P1 is vacant)
                        for j in stsnoms2:
                            cnt+=1
                            tmp=self.initialdict[mult_listP2][i]['sts'][j]
                            del tmp[0]
                            hsnom=tmp.pop(0)
                            outp=[hsnom,cnt,'','P1 vacancy','','','','']
                            p1totvac['sts']+=1
                            for u in tmp:
                                outp.append(u)
                            stsfinlist.append(outp)
                        #now full vacancies
                        vacsts=houseinfo[abbrv]['partialcap']['sts']-cnt
                        if vacsts>0:
                            for j in range(vacsts):
                                cnt+=1
                                tmp=['HIP sts',cnt,'FULLY VACANT','','','','','','','']
                                p1totvac['sts']+=1
                                p2totvac['sts']+=1
                                stsfinlist.append(tmp)
                        elif vacsts<0:
                            #print('   (ERROR!) HIP sts has negative vacancies?')
                            self.outputcommentlist.append('(ERROR) HIP sts has negative vacancies? '
                                                     'Change partialcap listing at top of script'
                                                     ' to fix this issue (rooms cnted='+str(cnt)+
                                                     ' and sts capacity='+str(houseinfo[abbrv]['partialcap']['sts']))
                        houseinfo[abbrv]['cap']="lgs:"+str(houseinfo[abbrv]['partialcap']['lgs'])+\
                                                ", sts:"+str(houseinfo[abbrv]['partialcap']['sts'])
                        finaldict[i]['Per1vacs']="lgs:"+str(p1totvac['lgs'])+", sts:"+str(p1totvac['sts'])
                        finaldict[i]['Per2vacs']="lgs:"+str(p2totvac['lgs'])+", sts:"+str(p2totvac['sts'])
                        for j in stsfinlist: #now load stsfinlist into finlist
                            finlist.append(j)
                    else: #this shouldnt be anything...
                        print 'sorry not doing ',i
                        self.errorlist.append('DID NOT recognize house "'+str(i)+'"')
                        continue
                    #this is final routine thing for all exceptions
                    finlist.append(['','','','','','','',''])
                    title=str(i)+' has a capacity of '+str(houseinfo[abbrv]['cap'])+'.'
                    if (finaldict[i]['Per1vacs'] not in [0,'0 ']) or (finaldict[i]['Per2vacs'] not in [0,'0 ']):
                        title+=' Vacancies exist = P1: '+str(finaldict[i]['Per1vacs'])+' P2: '+str(finaldict[i]['Per2vacs'])
                    else:
                        title+=' No Vacancies.'
                    finlist.insert(0,[title,'','','','','','',''])
                    finaldict[i]['output']=finlist
            self.finaldict=finaldict
        else: #do Fall/Spring
            for i in self.initialdict.keys():
                finaldict[i] = {}
            for i in self.initialdict.keys():
                print i
                finlist=[]
                vacnamelist=[] #for summary of rooms with vacancies, only for excpections?
                abbrv=self.getabbrv(i)
                if abbrv not in exceptionlist:
                    noms=self.initialdict[i].keys()
                    noms.sort()
                    for j in noms:  #check if any of names are on cancelations list; is this still neccessary?
                        if j in self.cancellist['other'].keys():
                            noms.remove(j)
                        elif j in self.cancellist['R&B'].keys():
                            noms.remove(j)
                    finaldict[i]['currcap']=len(noms)
                    finaldict[i]['vacs']=int(houseinfo[abbrv]['cap'])-int(len(noms))
                    if finaldict[i]['vacs']<0:
                        self.errorlist.append(str(i)+' has '+str(-finaldict[i]['vacs'])+
                                              ' more people than it should have. Check the capacity assignments at top of Broberg HL script')
                    elif finaldict[i]['vacs']>0:
                        if 'Cancellations' not in i:
                            self.outputcommentlist.append('Found '+str(finaldict[i]['vacs'])+' vacancies at '+str(i))
                    cnt=0
                    gender_cntr={'m':0,'f':0}
                    gq_vac_cntr = {'m':0,'f':0} #this is abstract and depends on gquota -> vacancies in list dont depend on this
                    vac_cntr={'m':0,'f':0}
                    for j in noms:
                        cnt+=1
                        tmp=self.initialdict[i][j]
                        tmp[1]=cnt
                        finlist.append(tmp)
                        gndr = self.getgender(tmp)
                        gender_cntr[gndr]+=1
                    for gndr in ['m','f']:
                        gdiff = houseinfo[abbrv]['gquota'][gndr] - gender_cntr[gndr]
                        if gdiff < 0:
                            self.errorlist.append('At '+str(i)+' you have exceeded gender quota by '+str(-gdiff))
                        else:
                            gq_vac_cntr[gndr] = gdiff
                    for j in range(finaldict[i]['vacs']):
                        cnt+=1
                        tmp=[abbrv,cnt,'','','','','','']
                        if gq_vac_cntr['m']:
                            tmp[2] = 'Male Vacancy'
                            gq_vac_cntr['m'] -= 1
                            vac_cntr['m']+=1
                        elif gq_vac_cntr['f']:
                            tmp[2] = 'Female Vacancy'
                            gq_vac_cntr['f'] -= 1
                            vac_cntr['f']+=1
                        else:
                            tmp[2] = 'Unknown Vacancy'
                            vac_cntr['m']+=1
                        finlist.append(tmp)
                    finlist.append(['','','','','','','',''])
                    title=str(i)+' has a capacity of '+str(houseinfo[abbrv]['cap'])+'.'
                    if finaldict[i]['vacs']:
                        title+=' Vacancies exist = '+str(finaldict[i]['vacs'])+' (male: '+str(vac_cntr['m'])+\
                                                                              ', female: '+str(vac_cntr['f'])+')'
                    else:
                        title+=' No Vacancies.'
                    finlist.insert(0,[title,'','','','','','',''])
                    finaldict[i]['output']=finlist
                else: #exceptions...
                    if abbrv=='FEN':
                        def makeroom(numstr):
                            rmout=[]
                            cnt=0
                            keylis=self.initialdict[i][int(numstr)].keys()
                            keylis.sort()
                            for j in keylis:
                                cnt+=1
                                out=self.initialdict[i][int(numstr)][j]
                                out[1]=cnt
                                rmout.append(out)
                            if numstr in houseinfo[abbrv]['poss_share']:
                                if len(keylis)==2:
                                    thiscap=2
                                    #print('   Making room '+str(numstr)+' a shared room')
                                    self.outputcommentlist.append('In Fenwick making room '+str(numstr)+' a shared room')
                                else:
                                    thiscap=1
                            else:
                                thiscap=houseinfo[abbrv]['partialcap'][numstr]
                            vacs=thiscap-len(rmout)
                            if vacs:
                                vacnamelist.append([vacs,u])
                                #print('   Room '+str(numstr)+' has '+str(vacs)+' vacancies')
                                self.outputcommentlist.append('In Fenwick, Room '+str(numstr)+' has '+str(vacs)+' vacancies')
                            for j in range(vacs):
                                cnt+=1
                                rmout.append(['Fen '+str(numstr),str(cnt),'','','','','',''])
                            rmout.append(['','','','','','','',''])
                            return vacs,rmout
                        totvac=0
                        vacstr='(room '
                        rmnums=houseinfo[abbrv]['partialcap'].keys()
                        rmnums.sort()
                        for u in rmnums:
                            vcs,ot=makeroom(u)
                            totvac+=vcs
                            if vcs<0:
                                self.errorlist.append('Fenwick '+str(u)+' has '+str(-vcs)+
                                                      ' more rooms than it should. Need to change capacity settings for Fenwick...')
                                for v in range(len(ot)):
                                    ot[v][0]='*'+str(ot[v][0])
                            elif vcs>0:
                                vacstr+=str(u)+' '
                            for v in ot:
                                finlist.append(v)
                        if vacstr!='(room ':
                            vacstr=vacstr[:-1]+')'
                        else:
                            vacstr=''
                        finaldict[i]['vacs']=str(totvac)+' '+vacstr
                    elif abbrv=='ROC':
                        def makeroom(numstr):
                            rmout=[]
                            cnt=0
                            keylis=self.initialdict[i][numstr].keys()
                            keylis.sort()
                            for j in keylis:
                                cnt+=1
                                out=self.initialdict[i][numstr][j]
                                out[1]=cnt
                                rmout.append(out)
                            thiscap=houseinfo[abbrv]['partialcap'][numstr]
                            vacs=thiscap-len(rmout)
                            if vacs:
                                vacnamelist.append([vacs,u])
                                #print('   Room '+str(numstr)+' has '+str(vacs)+' vacancies')
                                self.outputcommentlist.append('In Rochdale, Room '+str(numstr)+' has '+str(vacs)+' vacancies')
                            for j in range(vacs):
                                cnt+=1
                                rmout.append(['Roc '+str(numstr),str(cnt),'','','','','',''])
                            rmout.append(['','','','','','','',''])
                            return vacs,rmout
                        totvac=0
                        vacstr='(room '
                        rmnums=houseinfo[abbrv]['partialcap'].keys()
                        rmnums.sort()
                        for u in rmnums:
                            vcs,ot=makeroom(u)
                            totvac+=vcs
                            if vcs<0:
                                self.errorlist.append('Rochdale '+str(u)+' has '+str(-vcs)+
                                                      ' more rooms than it should. Need to change capacity settings for Rochdale...')
                                for v in range(len(ot)):
                                    ot[v][0]='*'+str(ot[v][0])
                            elif vcs>0:
                                vacstr+=str(u)+' '
                            for v in ot:
                                finlist.append(v)
                        if vacstr!='(room ':
                            vacstr=vacstr[:-1]+')'
                        else:
                            vacstr=''
                        finaldict[i]['vacs']=str(totvac)+' '+vacstr
                    elif abbrv=='NSC':
                        def makeroom(num):
                            rmout=[]
                            cnt=0
                            if float(num) not in self.initialdict[i].keys():
                                cnt+=1
                                vac=1
                                rmout.append(['NSC '+str(int(num)),1,'','','','','',''])
                            else:
                                vac=0
                                keylis=self.initialdict[i][num].keys()
                                keylis.sort()
                                for j in keylis:
                                    cnt+=1
                                    out=self.initialdict[i][num][j]
                                    out[1]=cnt
                                    rmout.append(out)
                            if (num in nsc_studios and cnt>1):
                                #print('   Room '+str(num)+' at NSC is a studio but has '+str(cnt)+' people.')
                                self.errorlist.append('Room '+str(num)+' at NSC is a studio but has '+str(cnt)+' people.')
                                for v in range(len(rmout)):
                                    ot[v][0]='*'+str(ot[v][0])
                            elif cnt>2:
                                #print('   Room '+str(num)+' at NSC is a studio but has more than one person.')
                                self.errorlist.append('Room '+str(num)+' at NSC is a studio but has more than one person.')
                            elif cnt==0:
                                vacnamelist.append([1,num])
                                print('   Room '+str(num)+' has a vacancy')
                                vac=1
                                cnt+=1
                                rmout.append(['NSC '+str(num),str(cnt),'','','','','',''])
                            rmout.append(['','','','','','','',''])
                            return vac,cnt,rmout
                        totvac=0
                        vacstr='(room '
                        totcap=0
                        rmnums=list(set(nsc_studios) | set(nsc_otherrooms))
                        rmnums.sort()
                        for u in rmnums:
                            vcs,capnum,ot=makeroom(u)
                            totcap+=capnum
                            totvac+=vcs
                            if vcs>0:
                                vacstr+=str(u)+' '
                            for v in ot:
                                finlist.append(v)
                        if vacstr!='(room ':
                            vacstr=vacstr[:-1]+')'
                        else:
                            vacstr=''
                        houseinfo[abbrv]['cap']=totcap
                        finaldict[i]['vacs']=str(totvac)+' '+vacstr
                    elif abbrv=='HIP':
                        totvac={'lgs':0,'sts':0}
                        if 'SHAREDROOM' in self.initialdict[i]['lgs'].keys():
                            cnt=1
                            tmpcnt=0 #for changing cnt number if multiple shared rooms exist
                            for j in self.initialdict[i]['lgs']['SHAREDROOM']:
                                tmpcnt+=1 #for changing room number in multi shared rooms
                                if (1+(tmpcnt-1.)/2.)==cnt+1:
                                    cnt+=1
                                j[0]='*'+j[0]
                                finlist.append(j)
                        else:
                            cnt=0
                        #do deluxes
                        keylis=self.initialdict[i]['lgs'].keys()
                        keylis.sort()
                        for u in keylis:
                            if u=='SHAREDROOM':
                                continue
                            cnt+=1
                            out=self.initialdict[i]['lgs'][u]
                            out[1]=cnt
                            finlist.append(out)
                        newcnt=cnt
                        if 'SHAREDROOM' in keylis:
                            cnt+=len(self.initialdict[i]['lgs']['SHAREDROOM'])/2
                        houseinfo[abbrv]['cap']=cnt
                        vaclgs=houseinfo[abbrv]['partialcap']['lgs']-cnt
                        for u in range(vaclgs):
                            newcnt+=1
                            totvac['lgs']+=1
                            finlist.append(['HIP lgs',newcnt,'','','','','',''])
                        finlist.append(['','','','','','','',''])
                        if vaclgs:
                            vacnamelist.append([vaclgs,'lgs'])
                        #now do standards
                        cnt=0
                        keylis=self.initialdict[i]['sts'].keys()
                        keylis.sort()
                        for u in keylis:
                            cnt+=1
                            out=self.initialdict[i]['sts'][u]
                            out[1]=cnt
                            finlist.append(out)
                        vacsts=houseinfo[abbrv]['partialcap']['sts']-cnt
                        houseinfo[abbrv]['cap']+=cnt
                        for u in range(vacsts):
                            cnt+=1
                            totvac['sts']+=1
                            finlist.append(['HIP sts',cnt,'','','','','',''])
                        finlist.append(['','','','','','','',''])
                        if vacsts:
                            vacnamelist.append([vacsts,'sts'])
                        finaldict[i]['vacs']="lgs:"+str(totvac['lgs'])+", sts:"+str(totvac['sts'])
                    else:
                        finaldict[i]['vacs']=0
                        continue
                    title=str(i)+' has a capacity of '+str(houseinfo[abbrv]['cap'])+'.'
                    if finaldict[i]['vacs'] and finaldict[i]['vacs']!='0 ':
                        title+=' Vacancies exist = '+str(finaldict[i]['vacs'])
                    else:
                        title+=' No Vacancies.'
                    if vacnamelist:
                        title+=' ('
                        for u in vacnamelist:
                            title+=str(u[0])+' in '+str(u[1])+', '
                        title=title[:-2]+')'
                    finlist.insert(0,[title,'','','','','','',''])
                    finaldict[i]['output']=finlist
            self.finaldict=finaldict
            return
    def finalprintout(self):
        cancelout=[['CANCELATION HOUSE','','','','','','','']]
        for i in ['other','R&B']:
                noms=self.cancellist[i].keys()
                noms.sort() #alphabetical
                for j in noms:
                    cancelout.append(self.cancellist[i][j])
        if self.sumflag:
            firstline = 'Berkeley Student Coop - Summer          house list made ' + str(time.asctime())
            blanks=['','','','','','','','']
            vactitle=['Vacancy Summary','','','','','','','']
            vacsummary=['House :']
            vaccntlisp1=['Vacancies P1:']
            vaccntlisp2=['Vacancies P2:']
            cntlis=0
            #print 'vacancies'
            for i in self.finaldict.keys():
                print i
                if self.finaldict[i]['Per1vacs'] or self.finaldict[i]['Per2vacs']:
                    vacsummary.append(str(i))
                    vaccntlisp1.append(self.finaldict[i]['Per1vacs'])
                    vaccntlisp2.append(self.finaldict[i]['Per2vacs'])
                    cntlis+=1
            outcolumns = ['loc', 'bed', 'st', 'name', 'cmnt', 'app', 'email', 'pts', 'st',
                          'name', 'cmnt', 'app', 'email', 'pts']
            labelPeriods=['Period1','','','','','','','','Period2','','','','','','','']
            if not cntlis:
                vacsummary.append('No vacancys exist for either Period')
                finaloutput=[[str(firstline),'','','','','','',''],vactitle,vacsummary,blanks,labelPeriods,outcolumns]
            else:
                finaloutput=[[str(firstline),'','','','','','',''],vactitle,vacsummary,vaccntlisp1,vaccntlisp2,blanks,labelPeriods,outcolumns]
            noms=self.finaldict.keys()
            noms.sort()
            for i in noms:
                if 'output' not in self.finaldict[i].keys():
                    continue
                for j in self.finaldict[i]['output']:
                    finaloutput.append(j)
            for j in cancelout:
                finaloutput.append(j)
        else: #if not summer
            firstline = 'Berkeley Student Coop -          house list made ' + str(time.asctime())
            vactitle=['Vacancy Summary','','','','','','','']
            vacsummary=['House :']
            vaccntlis=['Vacancies:']
            cntlis=0
            for i in self.finaldict.keys():
                if self.finaldict[i]['vacs']:
                    vacsummary.append(str(i))
                    vaccntlis.append(self.finaldict[i]['vacs'])
                    cntlis+=1
            if not cntlis:
                vacsummary.append('No vacancys exist')
            outcolumns = ['loc', 'bed', 'st', 'name', 'cmnt', 'app', 'email', 'pts']
            #ACA	1	S	Abbott, Kathleen (f)		134259	katyabbott@berkeley.edu	2.75
            blanks=['','','','','','','','']
            finaloutput=[[str(firstline),'','','','','','',''],vactitle,vacsummary,vaccntlis,blanks,outcolumns]
            noms=self.finaldict.keys()
            noms.sort()
            for i in noms:
                if 'output' not in self.finaldict[i].keys():
                    continue
                for j in self.finaldict[i]['output']:
                    finaloutput.append(j)
            for j in cancelout:
                finaloutput.append(j)
        if self.COrun:
            with open('C:\\' + str(exptlist), 'w') as myfile:
                write = csv.writer(myfile, lineterminator="\n")
                write.writerows(finaloutput)
        else:
            with open(str(exptlist),'w') as myfile:
                write = csv.writer(myfile, lineterminator="\n")
                write.writerows(finaloutput)
        print('\n')
        if self.outputcommentlist:
            print 'output messages:'
            for i in self.outputcommentlist:
                print(i)
        if not self.errorlist:
            print("\nNo global errors! Find corrected list in C:"+str(exptlist))
        else:
            print('\nERRORS FOUND:')
            for i in self.errorlist:
                print(i)



#s = FullHouse(in_nom='Fall2016/RMSfulllist.csv',COrun=False)
#s = FullHouse(in_nom='Summer2016/RMSfulllistSum.csv',COrun=False)
#s = FullHouse(in_nom='RMSfulllistSum1.csv',COrun=False)
s = FullHouse(in_nom=RMSlistname,COrun=False)
s.loadfile()
s.parsefile()
s.getfinaldict()
s.finalprintout()
