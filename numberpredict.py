from random import random,randint
import math

def wineprice(rating,age):
    peak_age=float(rating-50)
    price=rating/2
    if age>peak_age:
        price=price*(5-(age-peak_age))
    else:
       price=price*(5*(age+1)/peak_age)    
    if price<0:price=0
    print price
    return price

def wineset1():
    rows=[]
    for i in range(200):
        rating=50+50*random()
        age=random()*50
        aisle=float(randint(1,20))
        bottlesize=[375.0,750.0,1500.0,3000.0][randint(0,3)]
        price=wineprice(rating,age)
        price*=(bottlesize/750)
        price*=(0.1*random()+0.9)  
        rows.append({'input':(rating,age,aisle,bottlesize),'result':price}) 
    return rows

def wineset3():
    rows=wineset1()
    for row in rows:
        if random()<0.5:
            row['result']*=0.5
    return rows        

def euclidean(v1,v2):
    d=sum([ ( v1[i]-v2[i] )**2  for i in range(len(v1))]) 
    return math.sqrt(d)
    
def getdistances(data,vec1):
    distancelist=[]
    for i in range(len(data)):
        vec2=data[i]['input']
        distancelist.append((euclidean(vec1,vec2),i))
    distancelist.sort()
    return distancelist    

def knnestimate(data,vec1,k=5):
    dlist=getdistances(data,vec1)
    avg=0.0
    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]['result'] 
    avg=avg/k
    return avg    

def inverseweight(dist,num=1.0,const=0.1):
    return num/(dist+const)

def subtractweight(dist,const=1.0):
    if dist>const:
        return 0.0
    return const - dist            
def gaussian(dist,sigma=10.0):
    return math.e**(-dist**2/(2*sigma**2))

def weightedknn(data,vec1,k=3,weightf=gaussian):
    dlist=getdistances(data,vec1)
    avg=0.0
    totalweight=0.0

    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg += weight*data[idx]['result'] 
        totalweight+=weight
    avg = avg/totalweight
    return avg    
def dividedata(data,test=0.05):
    trainset=[]
    testset=[]
    for row in data:
        if random()<test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset,testset            

def testalgorithm(algf,trainset,testset):
    error=0.0
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2
    return error/len(testset)
def crossvalidate(algf,data,trials=100,test=0.05):
    error=0.0
    for i in range(trials):
        trainset,testset=dividedata(data,test)
        error+=testalgorithm(algf,trainset,testset)
    return error/trials        

def rescale(data,scale):
    scaleddata=[]
    for row in data:
        scaled=[ scale[i]*row['input'][i]  for i in range(len(scale))]
        scaleddata.append({'input':scaled,'result':row['result']})
    return scaleddata 

def createcostfunction(algf,data):
    def costf(scale):
        sdata=rescale(data,scale)
        return crossvalidate(algf,sdata,trials=10)
    return costf

def probguess(data,vec1,low,high,k=5,weightf=gaussian):
    dlist=getdistances(data,vec1)
    nweight=0.0
    tweight=0.0
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        v=data[idx]['result']
        if v >=low and v<=high:
            nweight+=weight
        tweight+=weight
    if tweight==0:
        return 0
    return nweight/tweight             
        
if __name__=='__main__':
    print wineprice(95.0,3.0)          
    print wineprice(95.0,8.0)          
    print wineprice(98.0,1.0)
    
    data=wineset1()
    print data[0]
    print data[1]
    print euclidean(data[0]['input'],data[1]['input'] )
    print "real 99.0,5.0",wineprice(99.0,5.0)        
    print knnestimate(data,(95.0,5.0))        
    print knnestimate(data,(95.0,5.0),k=1)
    
    print inverseweight(0.1)
    print subtractweight(0.1)
    print gaussian(0.1)
    print weightedknn(data,(99.0,5.0),k=3)
    
    def knn3(d,v):return knnestimate(d,v,k=3)
    def knn1(d,v):return knnestimate(d,v,k=1)
    #print crossvalidate(knnestimate,data)
    print crossvalidate(knn3,data)
    #print crossvalidate(knn1,data)
    #print crossvalidate(weightedknn,data)
    sdata=rescale(data,[10,10,0,0.5])
    print data[0],sdata[0]
    print crossvalidate(knn3,sdata)

    import optimization
    weightdomain=[ (0,20) ]*4
    costf=createcostfunction(knnestimate,data)
    print "begin optimize"
    #print optimization.annealingoptimize(weightdomain,costf,step=2)

    data=wineset3()
    print wineprice(99.0,20.0)
    print weightedknn(data,[99.0,22.0])

    print probguess(data,[99,20],0,80)
    print probguess(data,[99,20],80,420)
    print probguess(data,[99,20],420,1000)
    print probguess(data,[99,20],30,120)
