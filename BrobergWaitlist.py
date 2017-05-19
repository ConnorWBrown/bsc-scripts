"""
inputs = Initialfile.csv

This is combined Broberg waitlist script
version = 1.1, may 2, 2017 (fixed some bugs for CO)

Idea is to combine and simplify:
    - this is for waitlist script - so no user modification needed (by betsy/kyle)
    - work for all semesters (identify when summer and when fall...)
    - merge all concepts into workable classes for better functionality
    - get rid of excessive printing
    - eventually print errors to the csv file?
"""

import os
import csv

mult_list="Initialfile.csv"


class FullWaitlist(object):
    """
    Class that implements all methods for Waitlist Output
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
        self.initiallist={}
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
        self.keylist=keylist
        if 'Application Period' in keylist:
            self.outputcommentlist.append('Determined this is Summer waitlist type')
            self.sumflag=True
            self.initiallistp2={}
        else:
            self.outputcommentlist.append('Determined this is Fall/Spring waitlist type')
            self.sumflag=False
        tmpinitial={} #this is dictionary with rows as keys
        delnum=0
        for i in range(1,len(tmpmultstuff)):
            tmpinitial[i]={}
            for j,k in zip(keylist,tmpmultstuff[i]):
                tmpinitial[i][j]=k
            if tmpinitial[i]['Application Cancel Date']:
                delnum+=1
                del tmpinitial[i]
                continue
            appnum=tmpinitial[i]['BSC Application Number']
            if self.sumflag: #summer
                if ('Full' in tmpinitial[i]['Application Period']) or ('Period 1' in tmpinitial[i]['Application Period']):
                    if appnum not in self.initiallist.keys():
                        self.initiallist[appnum]=[]
                    self.initiallist[appnum].append(tmpinitial[i])
                elif 'Period 2' in tmpinitial[i]['Application Period']:
                    if appnum not in self.initiallistp2.keys():
                        self.initiallistp2[appnum]=[]
                    self.initiallistp2[appnum].append(tmpinitial[i])
                else:
                    self.errorlist.append("ERROR. Could not find Application Period type for "+str(appnum))
            else: #sp/fa type
                if appnum not in self.initiallist.keys():
                    self.initiallist[appnum]=[]
                self.initiallist[appnum].append(tmpinitial[i])
        self.outputcommentlist.append('Deleted '+str(delnum)+' rows because they had Application Cancel Date values.')
        return
    def prefoutval(self,codevals):
        prefcode=codevals[1]
        if prefcode in ['ACA','PRO','CAZ','CLO','CON','DAV','EUC','HOY','KID','KNG','LOT','RID','SHE','STB','WAR','WOL','WAR']:
            return prefcode
        elif prefcode=='WIL':
            return 'WAR'
        elif prefcode=='ATH':
            return 'PRO'
        elif prefcode=='HIP':
            if 'STD' in codevals[2].upper():
                return 'HIP sts'
            elif 'DLX' in codevals[2].upper():
                return 'HIP lgs'
            else:
                return 'HIP'
        elif 'FEN' in prefcode:
            if 'Bedroom' in codevals[2]:
                bedlist=codevals[2].split()
                out='FEN '+bedlist[1]+'b'
                if str(bedlist[1])=='1':
                    if 'Shared' in bedlist:
                        out+='s'
                    else:
                        out+='a'
                return out
            else:
                return 'FEN'
        elif 'NSC' in prefcode:
            if 'Bedroom' in codevals[2]:
                bedlist=codevals[2].split()
                out='NSC '+bedlist[1]+'b'
                if str(bedlist[1])=='1':
                    if 'Shared' in bedlist:
                        out+='s'
                    else:
                        out+='a'
                return out
            elif 'Studio' in codevals[2]:
                return 'NSC st'
            else:
                return 'NSC'
        elif 'ROC' in prefcode:
            if 'Bedroom' in codevals[2]:
                bedlist=codevals[2].split()
                out='ROC '+bedlist[1]+'b'
                if str(bedlist[1])=='1':
                    if 'Shared' in bedlist:
                        out+='s'
                    else:
                        out+='a'
                return out
            elif 'Studio' in codevals[2]:
                return 'ROC st'
            else:
                return 'ROC'
        elif '' in prefcode:
                 return ''
        else:
                 print('Serious problem with preference assignment'+str(prefcode)+str(codevals[2])+', contact danny')
                 self.errorlist.append('Serious problem with preference assignment, contact danny. Issue was with'
                                       +str(prefcode)+str(codevals[2]))
    def prepare_preftypelists(self):
        preftypelist = {}
        for i in self.initiallist.keys():
            if len(self.initiallist[i]) == 1:
                if not self.initiallist[i][0]['Preference Code']:
                    self.initiallist[i][0]['Preference Code'] = 'NO PREFERENCES ON FILE!'
                else:
                    preflist= [int(self.initiallist[i][0]['Preference Number']),self.initiallist[i][0]['Preference Code'],
                               self.initiallist[i][0]['Preferred Room Type']]
                    self.initiallist[i][0]['Preference Code'] = self.prefoutval(preflist)
                preftypelist[i] = self.initiallist[i][0]
            else:
                preflist = []
                spacelist = [] #for listing unranked bed spaces
                for j in self.initiallist[i]:
                    try:
                        preflist.append([int(j['Preference Number']), j['Preference Code'], j['Preferred Room Type']])
                    except:
                        preflist.append([j['Preference Number'], j['Preference Code'], j['Preferred Room Type']])
                        #spacelist.append(j['Bed Space'])
                if len(spacelist):
                    print('Preference Number not specified for app number',j['BSC Application Number'],
                          ' in P1/P12 with bed space(s) ',spacelist)
                    self.errorlist.append('Preference Number not specified for app number '
                                          +str(j['BSC Application Number'])+' in P1/P12 with bed space(s) '+str(spacelist))
                preflist.sort()
                preffin = ''
                for j in preflist:
                    inpval = self.prefoutval(j)
                    preffin += str(inpval) + ','
                if not preffin:
                    preffin = 'NO PREFERENCES ON FILE!'
                else:
                    preffin = preffin[:-1]
                preftypelist[i] = {}
                for j in self.initiallist[i][0].keys():
                    if j == 'Preference Number':
                        preftypelist[i][j] = '1'
                    elif j == 'Preference Code':
                        preftypelist[i][j] = preffin
                    else:
                        preftypelist[i][j] = self.initiallist[i][0][j]
        self.preftypelist=preftypelist
        if self.sumflag:
            preftypelistp2={}
            for i in self.initiallistp2.keys():
                if len(self.initiallistp2[i]) == 1:
                    if not self.initiallistp2[i][0]['Preference Code']:
                        self.initiallistp2[i][0]['Preference Code'] = 'NO PREFERENCES ON FILE!'
                        preftypelistp2[i] = self.initiallistp2[i][0]
                    else:
                        preflist= [int(self.initiallistp2[i][0]['Preference Number']),
                                   self.initiallistp2[i][0]['Preference Code'], self.initiallistp2[i][0]['Preferred Room Type']]
                        self.initiallistp2[i][0]['Preference Code'] = self.prefoutval(preflist)
                    # preftypelist[i] = self.initiallistp2[i][0] #THIS IS ROLL OVER FROM EARLIER PART OF CODE - PRODUCES ERROR
                else:
                    preflist = []
                    spacelist=[]
                    for j in self.initiallistp2[i]:
                        try:
                            preflist.append([int(j['Preference Number']), j['Preference Code'], j['Preferred Room Type']])
                        except:
                            preflist.append([j['Preference Number'], j['Preference Code'], j['Preferred Room Type']])
                            spacelist.append(j['Bed Space'])
                    if len(spacelist):
                        print('Preference Number not specified for app number',j['BSC Application Number'],
                              ' in P2 with bed space(s) ',spacelist)
                        self.errorlist.append('Preference Number not specified for app number '
                                              +str(j['BSC Application Number'])+' in P2 with bed space(s) '+str(spacelist))
                    preflist.sort()
                    preffin = ''
                    for j in preflist:
                        inpval = self.prefoutval(j)
                        preffin += str(inpval) + ','
                    if not preffin:
                        preffin = 'NO PREFERENCES ON FILE!'
                    else:
                        preffin = preffin[:-1]
                    preftypelistp2[i] = {}
                    for j in self.initiallistp2[i][0].keys():
                        if j == 'Preference Number':
                            preftypelistp2[i][j] = '1'
                        elif j == 'Preference Code':
                            preftypelistp2[i][j] = preffin
                        else:
                            preftypelistp2[i][j] = self.initiallistp2[i][0][j]
            self.preftypelistp2=preftypelistp2
        self.outputcommentlist.append("Reordered preference lists.")
        return
    def organize_wl(self,dumb_override=False):
        #dumb override allows you to skip all organizing and just make gendered lists based on points
        #order into male and female
        mediumorg_mlist = {}
        mediumorg_flist = {}
        for i in self.preftypelist.keys():
            now = self.preftypelist[i]
            if now['Sex Identification'] == 'Man':
                mediumorg_mlist[i] = now
            elif now['Sex Identification'] == 'Woman':
                mediumorg_flist[i] = now
            else:
                self.errorlist.append('Sex identification of app num ' + str(i) + ' was ' + str(
                    now['Sex Identification']) + '. Added them to female waitlist...')
                mediumorg_flist[i] = now
        if self.sumflag:
            mediumorg_mlistp2 = {}
            mediumorg_flistp2 = {}
            for i in self.preftypelistp2.keys():
                now = self.preftypelistp2[i]
                if now['Sex Identification'] == 'Man':
                    mediumorg_mlistp2[i] = now
                elif now['Sex Identification'] == 'Woman':
                    mediumorg_flistp2[i] = now
                else:
                    self.errorlist.append('Sex identification of app num ' + str(i) + ' was ' + str(
                        now['Sex Identification']) + '. Added them to female waitlist...')
                    mediumorg_flistp2[i] = now
            self.outputcommentlist.append(
                '(P1/P12) Gender lists have been assigned. Females=' + str(len(mediumorg_flist)) + ', Males=' + str(len(mediumorg_mlist)))
            self.outputcommentlist.append(
                '(P2) Gender lists have been assigned. Females=' + str(len(mediumorg_flistp2)) + ', Males=' + str(len(mediumorg_mlistp2)))
        else:
            self.outputcommentlist.append('Gender lists have been assigned. Females='+str(len(mediumorg_flist))+', Males='+str(len(mediumorg_mlist)))
        #organize for points
        final_mlist = []
        for i in mediumorg_mlist.keys():
            if float(mediumorg_mlist[i]['Points']):
                tmp = []
                for j in self.keylist:
                    tmp.append(mediumorg_mlist[i][j])
                final_mlist.append(tmp)
                del mediumorg_mlist[i]  #THIS IS WHERE ERROR IS - DONT DELETE THIS
            else:
                continue
        final_flist = []
        for i in mediumorg_flist.keys():
            if float(mediumorg_flist[i]['Points']):
                tmp = []
                for j in self.keylist:
                    tmp.append(mediumorg_flist[i][j])
                final_flist.append(tmp)
                del mediumorg_flist[i]
            else:
                continue
        ptsind=self.keylist.index('Points')
        appind=self.keylist.index('BSC Application Number')
        final_mlist=sorted(final_mlist, key=lambda x:(-float(x[ptsind]),x[appind]))  #sorts points, with app number as well
        final_flist=sorted(final_flist, key=lambda x:(-float(x[ptsind]),x[appind]))  #sorts points, with app number as well
        # for i in [final_mlist, final_flist]:
        #     for j in i:
        #         j.pop(0)  #remove the sorting thing because we dont want it first
        if self.sumflag:
            final_mlistp2 = []
            for i in mediumorg_mlistp2.keys():
                if float(mediumorg_mlistp2[i]['Points']):
                    #tmp = [float(mediumorg_mlistp2[i]['Points'])]  #put points at front to make sorting easy
                    tmp = []
                    for j in self.keylist:
                        tmp.append(mediumorg_mlistp2[i][j])
                    final_mlistp2.append(tmp)
                    del mediumorg_mlistp2[i]
                else:
                    continue
            final_flistp2 = []
            for i in mediumorg_flistp2.keys():
                if float(mediumorg_flistp2[i]['Points']):
                    #tmp = [float(mediumorg_flistp2[i]['Points'])]
                    tmp = []
                    for j in self.keylist:
                        tmp.append(mediumorg_flistp2[i][j])
                    final_flistp2.append(tmp)
                    del mediumorg_flistp2[i]
                else:
                    continue
            final_mlistp2=sorted(final_mlistp2, key=lambda x:(-float(x[self.keylist.index('Points')]),
                                                              x[self.keylist.index('BSC Application Number')]))  #sorts points, with app number as well
            final_flistp2=sorted(final_flistp2, key=lambda x:(-float(x[self.keylist.index('Points')]),
                                                              x[self.keylist.index('BSC Application Number')]))
        if dumb_override:
            #this means we are just sorting according to points...not caring about all other stuff?
            #print all extras...
            genlisttypes=[mediumorg_mlist,mediumorg_flist]
            outlists=[final_mlist,final_flist]
            if self.sumflag:
                genlisttypes.append(mediumorg_mlistp2)
                outlists.append(final_mlistp2)
                genlisttypes.append(mediumorg_flistp2)
                outlists.append(final_flistp2)
            for i,outf in zip(genlisttypes,outlists):
                for j in i.keys():
                    tmp=[]
                    for k in self.keylist:
                        tmp.append(i[j][k])
                    outf.append(tmp)
        else:
            #normal sorts EOP etc...
            #Males first
            eopdsplist = []
            boardlist = []
            eapcooplist = []
            otherlist = []
            nonelist = []  #dont have any of classifiers
            if self.sumflag:
                eopdsplistp2 = []
                boardlistp2 = []
                eapcooplistp2 = []
                otherlistp2 = []
                nonelistp2 = []  #dont have any of classifiers
            for i in mediumorg_mlist.keys():
                now = mediumorg_mlist[i]
                tmp = []
                for j in self.keylist:
                    tmp.append(now[j])
                if (now['EOP Verification'] == 'Y' or now['DSP Verification'] == 'Y' or now[
                    'Transfer Student Verification (Y)'] == 'Y' or now['AB540 Verification (Y)'] == 'Y'):
                    eopdsplist.append(tmp)
                elif now['Boarder'] == 'Y':
                    boardlist.append(tmp)
                elif now['EAP Verification'] == 'Y':
                    eapcooplist.append(tmp)
                elif now['Other Co-op Verification'] == 'Y':
                    otherlist.append(tmp)
                else:
                    nonelist.append(tmp)
            if self.sumflag:
                for i in mediumorg_mlistp2.keys():
                    now = mediumorg_mlistp2[i]
                    tmp = []
                    for j in self.keylist:
                        tmp.append(now[j])
                    if (now['EOP Verification'] == 'Y' or now['DSP Verification'] == 'Y' or now[
                        'Transfer Student Verification (Y)'] == 'Y' or now['AB540 Verification (Y)'] == 'Y'):
                        eopdsplistp2.append(tmp)
                    elif now['Boarder'] == 'Y':
                        boardlistp2.append(tmp)
                    elif now['EAP Verification'] == 'Y':
                        eapcooplistp2.append(tmp)
                    elif now['Other Co-op Verification'] == 'Y':
                        otherlistp2.append(tmp)
                    else:
                        nonelistp2.append(tmp)
            eopdsplist.sort()
            boardlist.sort()
            eapcooplist.sort()
            otherlist.sort()
            nonelist.sort()
            for i in [eopdsplist, boardlist, eapcooplist, otherlist, nonelist]:
                for j in i:
                    final_mlist.append(j)
            if self.sumflag:
                eopdsplistp2.sort()
                boardlistp2.sort()
                eapcooplistp2.sort()
                otherlistp2.sort()
                nonelistp2.sort()
                for i in [eopdsplistp2, boardlistp2, eapcooplistp2, otherlistp2, nonelistp2]:
                    for j in i:
                        final_mlistp2.append(j)
            #Now females
            eopdsplist = []
            boardlist = []
            eapcooplist = []
            otherlist = []
            nonelist = []  #dont have any of classifiers
            if self.sumflag:
                eopdsplistp2 = []
                boardlistp2 = []
                eapcooplistp2 = []
                otherlistp2 = []
                nonelistp2 = []  #dont have any of classifiers
            for i in mediumorg_flist.keys():
                now = mediumorg_flist[i]
                tmp = []
                for j in self.keylist:
                    tmp.append(now[j])
                if (now['EOP Verification'] == 'Y' or now['DSP Verification'] == 'Y' or now[
                    'Transfer Student Verification (Y)'] == 'Y' or now['AB540 Verification (Y)'] == 'Y'):
                    eopdsplist.append(tmp)
                elif now['Boarder'] == 'Y':
                    boardlist.append(tmp)
                elif now['EAP Verification'] == 'Y':
                    eapcooplist.append(tmp)
                elif now['Other Co-op Verification'] == 'Y':
                    otherlist.append(tmp)
                else:
                    nonelist.append(tmp)
            if self.sumflag:
                for i in mediumorg_flistp2.keys():
                    now = mediumorg_flistp2[i]
                    tmp = []
                    for j in self.keylist:
                        tmp.append(now[j])
                    if (now['EOP Verification'] == 'Y' or now['DSP Verification'] == 'Y' or now[
                        'Transfer Student Verification (Y)'] == 'Y' or now['AB540 Verification (Y)'] == 'Y'):
                        eopdsplistp2.append(tmp)
                    elif now['Boarder'] == 'Y':
                        boardlistp2.append(tmp)
                    elif now['EAP Verification'] == 'Y':
                        eapcooplistp2.append(tmp)
                    elif now['Other Co-op Verification'] == 'Y':
                        otherlistp2.append(tmp)
                    else:
                        nonelistp2.append(tmp)
            eopdsplist.sort()
            boardlist.sort()
            eapcooplist.sort()
            otherlist.sort()
            nonelist.sort()
            for i in [eopdsplist, boardlist, eapcooplist, otherlist, nonelist]:
                for j in i:
                    final_flist.append(j)
            if self.sumflag:
                eopdsplistp2.sort()
                boardlistp2.sort()
                eapcooplistp2.sort()
                otherlistp2.sort()
                nonelistp2.sort()
                for i in [eopdsplistp2, boardlistp2, eapcooplistp2, otherlistp2, nonelistp2]:
                    for j in i:
                        final_flistp2.append(j)
            final_flist.insert(0, self.keylist)
            final_mlist.insert(0, self.keylist)
            if self.sumflag:
                final_flistp2.insert(0, self.keylist)
                final_mlistp2.insert(0, self.keylist)
            self.outputcommentlist.append('Priorities based on EOP etc. have been assigned.')
        self.final_flist=final_flist
        self.final_mlist=final_mlist
        if self.sumflag:
            self.final_flistp2=final_flistp2
            self.final_mlistp2=final_mlistp2
        return
    def finalprintout(self):
        if self.sumflag:
            exptlistM = "Correctedfile_sum_M.csv"
            exptlistF = "Correctedfile_sum_F.csv"
            exptlistFp2 = "Correctedfile_sum_F_P2.csv"
            exptlistMp2 = "Correctedfile_sum_M_P2.csv"
            keywillbe = [exptlistF, exptlistM, exptlistFp2, exptlistMp2]
            inwillbe = [self.final_flist, self.final_mlist, self.final_flistp2, self.final_mlistp2]
        else:
            exptlistM="Correctedfile_M.csv"
            exptlistF="Correctedfile_F.csv"
            keywillbe =[exptlistF, exptlistM]
            inwillbe = [self.final_flist, self.final_mlist]
        for j,k in zip(keywillbe,inwillbe):
            if self.COrun:
                with open('C:\\' + str(j), 'w') as myfile:
                    write = csv.writer(myfile, lineterminator="\n")
                    write.writerows(k)
            else:
                with open(str(j),'w') as myfile:
                    write = csv.writer(myfile, lineterminator="\n")
                    write.writerows(k)
        print('\n')
        if self.outputcommentlist:
            print('output messages:')
            for i in self.outputcommentlist:
                print(i)
        if not self.errorlist:
            print("No errors found!")
        else:
            print('ERRORS FOUND:')
            for i in self.errorlist:
                print(i)

#s = FullWaitlist(in_nom='Summer2016/Initialfile.csv',COrun=False)
# s = FullWaitlist(in_nom=mult_list,COrun=True)
s = FullWaitlist(in_nom='InitialfileMay2_17.csv',COrun=False)
s.loadfile()
s.prepare_preftypelists()
s.organize_wl(dumb_override=False)
s.finalprintout()
