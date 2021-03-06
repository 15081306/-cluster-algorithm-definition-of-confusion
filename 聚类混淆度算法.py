+#author:MingYu Pang
 +#time：2017/6/23
 +
 +#下面是一个类，通过输入数据集，聚类数，能得到5种算法的聚类数混淆情况。
 +#另外，在默认参数条件下，
 +#能实现DBSCAN以及Affinity Propagation算法的聚类混淆情况（这种情况，无须输入聚类数）
 +
 +class DrawCluster():
 +    def __init__(self,dataset,cluster_num=3):
 +        self.dataset=dataset    #数据集，dataset形式为pd
 +        self.cluster_num=cluster_num  #聚类数
 +        self.suanfa={}
 +        self.suanfa_PCA={}  #降维后的字典，储存算法聚类结果
 +        self.key=[]  #存储算法的名称,不包括DBSCAN以及AffinityPropogation
 +        self.keys=[]  #储存算法的名称，包括DBSCAN以及AffinityPropogation
 +        
 +        '''可通过下面的变量修改聚类算法的参数 '''  
 +        
 +        self.KMeans={'n_clusters':self.cluster_num,'init':'k-means++',
 +                    'compute_labels':True,'max_iter':100,'batch_size':100,
 +                    'tol':0.0,'max_no_improvement':10,'random_state':None,'verbose':0,
 +                    'init_size':None, 'n_init':3, 
 +                    'reassignment_ratio':0.01}
 +        
 +        self.AffinityPropagation={'damping':0.5,'max_iter':200, 'convergence_iter':15, 
 +                                 'copy':True, 'preference':None, 'affinity':'euclidean', 'verbose':False}
 +        
 +        self.SpectralClustering={'n_clusters':self.cluster_num, 'eigen_solver':None, 'random_state':None, 
 +                                'n_init':10, 'gamma':1.0, 'affinity':'rbf', 'n_neighbors':10, 
 +                                'eigen_tol':0.0, 'assign_labels':'kmeans', 'degree':3, 
 +                                'coef0':1, 'kernel_params':None, 'n_jobs':1}
 +        
 +        self.ward={'n_clusters':self.cluster_num, 'affinity':'euclidean', 
 +                                     'connectivity':None, 'compute_full_tree':'auto', 
 +                                     'linkage':'ward', 'pooling_func':np.mean}
 +        
 +        self.AgglomerativeClustering={'n_clusters':self.cluster_num, 'affinity':'euclidean',  
 +                                     'connectivity':None, 'compute_full_tree':'auto', 
 +                                     'linkage':'average', 'pooling_func':np.mean}
 +        
 +        self.DBSCAN={'eps':0.5, 'min_samples':5, 'metric':'euclidean', 
 +                    'algorithm':'auto', 'leaf_size':30, 'p':None, 'n_jobs':1}
 +        
 +        self.Birch={'threshold':0.5, 'branching_factor':50, 
 +                    'n_clusters':self.cluster_num, 'compute_labels':True, 'copy':True}
 +                    
 +
 +    def average(self,df,i,g):  #计算聚类中心到聚类样本点的平均距离，i代表第i个算法，g代表聚类数
 +        h={}
 +        if self.key[i]!='DBSCAN' and self.key[i]!='AffinityPropagation':
 +            ds=[] #平均距离
 +            for j in range(g):
 +                #开始计算平均距离
 +                lei=np.nonzero(self.suanfa[self.key[i]]['y_pred']==j)[0]
 +                if len(lei)==0:print(g)
 +                d=0
 +                for k in lei:
 +                    d=d+self.enlid(self.suanfa[self.key[i]]['centroids'][j],df.iloc[k,:])
 +                ds.append(d/len(lei))
 +        h=ds
 +        return h  
 +    
 +    #类似于求平均距离，我们求最大距离以及最小距离作为半径,i为第i个算法，t为聚类数
 +    def maxRminR1(self,df,i,t):
 +        h1=[]
 +        h0=[]
 +        if self.key[i]!='DBSCAN' and self.key[i]!='AffinityPropagation':
 +            dm=[] #最大距离
 +            di=[]#最小距离
 +            for j in range(t):
 +                #开始计算平均距离
 +                lei=np.nonzero(self.suanfa[self.key[i]]['y_pred']==j)[0]
 +                maxd=0
 +                minr=np.inf
 +                for k in lei:
 +                    d=self.enlid(self.suanfa[self.key[i]]['centroids'][j],df.iloc[k,:])
 +                    if maxd<d:maxd=d
 +                    if minr>d:minr=d
 +                dm.append(maxd)
 +                di.append(minr)
 +            h1=dm
 +            h0=di
 +        return h1,h0
 +    
 +    def enlid(self,inA,inB):  #求解欧氏距离
 +        dist = np.linalg.norm(inA - inB)  
 +        return dist
 +   
 +    #用于不对应于同算法画圆的函数，k是聚类数，H,Max,Min分别为圆的平均半径，最大半径，最小半径
 +    #平均半径，最大半径，最小半径分别由blue,black,yellow颜色绘制
 +    def plot_Circle(self,k,H,Max,Min):
 +        fig = plt.figure(figsize=(12,8))
 +        for i in range(len(self.key)):
 +            ax = fig.add_subplot(331+i)
 +            '''实现平均距离'''
 +            cirH=0
 +            cirMax=0
 +            cirMin=0 
 +            print("%s algorithm :Cluster number,Cluster shape after PCA:"%self.key[i])
 +            print(k,self.suanfa1[self.key[i]]['centroids'].shape)
 +            for t in range(k):
 +                #print(H[key[i]])
 +                #print(suanfa1[key[i]]['centroids'])
 +                #第一个参数为圆心坐标，第二个为半径 #第三个为透明度（0-1）
 +                cirH=Circle(xy = (self.suanfa1[self.key[i]]['centroids'][t][0],self.suanfa1[self.key[i]]['centroids'][t][1]), 
 +                              radius=H[self.key[i]][0][t], alpha=0.4) 
 +                ax.add_patch(cirH)
 +
 +                cirMax=Circle(xy = (self.suanfa1[self.key[i]]['centroids'][t][0],self.suanfa1[self.key[i]]['centroids'][t][1]), 
 +                              radius=Max[self.key[i]][0][t],color="black",alpha=0.4) 
 +                ax.add_patch(cirMax)
 +
 +                cirMin=Circle(xy = (self.suanfa1[self.key[i]]['centroids'][t][0],self.suanfa1[self.key[i]]['centroids'][t][1]), 
 +                              radius=Min[self.key[i]][0][t],color="yellow", alpha=0.4)
 +                ax.add_patch(cirMin)
 +
 +                plt.scatter(self.suanfa1[self.key[i]]['centroids'][t,0],
 +                            self.suanfa1[self.key[i]]['centroids'][t,1],marker='8',color="red")
 +
 +            plt.axis('scaled')
 +            plt.axis('equal') 
 +            plt.title(self.key[i])
 +        plt.show()
 +    
 +    def plot_Circle_special(self,H,Max,Min):
 +        fig = plt.figure(figsize=(12,8))
 +        key=['DBSCAN','AffinityPropagation']
 +        #print('blue--Average distance;black--Max distance;yellow--Min distance;')
 +        for i in range(2):
 +            print("%s algorithm :Cluster number,Cluster shape after PCA:"%key[i])
 +            print(len(self.suanfa[key[i]]['centroids']),self.suanfa1[key[i]]['centroids'].shape)
 +            ax = fig.add_subplot(332+i)
 +            '''实现平均距离'''
 +            cirH=0
 +            cirMax=0
 +            cirMin=0 
 +            p=len(self.suanfa[key[i]]['centroids'])
 +            for t in range(p):
 +                #print(H[key[i]])
 +                #print(suanfa1[key[i]]['centroids'])
 +                #第一个参数为圆心坐标，第二个为半径 #第三个为透明度（0-1）
 +                cirH=Circle(xy = (self.suanfa1[key[i]]['centroids'][t][0],self.suanfa1[key[i]]['centroids'][t][1]), 
 +                              radius=H[key[i]][0][t], alpha=0.4) 
 +                ax.add_patch(cirH)
 +
 +                cirMax=Circle(xy = (self.suanfa1[key[i]]['centroids'][t][0],self.suanfa1[key[i]]['centroids'][t][1]), 
 +                              radius=Max[key[i]][0][t],color="black",alpha=0.4) 
 +                ax.add_patch(cirMax)
 +
 +                cirMin=Circle(xy = (self.suanfa1[key[i]]['centroids'][t][0],self.suanfa1[key[i]]['centroids'][t][1]), 
 +                              radius=Min[key[i]][0][t],color="yellow", alpha=0.4)
 +                ax.add_patch(cirMin)
 +
 +                plt.scatter(self.suanfa1[key[i]]['centroids'][t,0],
 +                            self.suanfa1[key[i]]['centroids'][t,1],marker='8',color="red")
 +
 +            plt.axis('scaled')
 +            plt.axis('equal') 
 +            plt.title(key[i])       
 +        plt.show()
 +            
 +    
 +    #衡量各种算法的聚类个数均衡度，返回值为每种算法各个聚类的样本个数 (包括DBSCAN，AffinityPropagation)
 +    def Jun_level(self):
 +        keys=list(self.suanfa.keys())
 +        D={}
 +        for j in range(len(self.suanfa)): #多少种算法
 +            if keys[j]!='DBSCAN' and keys[j]!='AffinityPropagation':
 +                line=[]
 +                m=len(set(self.suanfa['MiniBatchKMeans']['y_pred']))  #多少聚类数
 +                for i in range(m):
 +                    p=np.nonzero(self.suanfa[keys[j]]['y_pred']==i)[0]
 +                    line.append(len(p))
 +                D[keys[j]]=line
 +            else:
 +                lei=list(set(self.suanfa[keys[j]]['y_pred']))
 +                line=[]
 +                for i in lei:
 +                    p=np.nonzero(self.suanfa[keys[j]]['y_pred']==i)[0]
 +                    line.append(len(p))
 +                D[keys[j]]=line
 +        print('聚类均衡性\n')
 +        print(D)
 +
 +    
 +    def special_algorithm(self):   #单独考虑DBSCAN以及Affinity算法
 +        dbscan = cluster.DBSCAN(eps=self.DBSCAN['eps'], min_samples=self.DBSCAN['min_samples'], 
 +                                metric=self.DBSCAN['metric'], algorithm=self.DBSCAN['algorithm'], 
 +                                leaf_size=self.DBSCAN['leaf_size'], p=self.DBSCAN['p'], n_jobs=self.DBSCAN['n_jobs'])
 +        
 +        affinity_propagation = cluster.AffinityPropagation(damping=self.AffinityPropagation['damping'], 
 +                                                           max_iter=self.AffinityPropagation['max_iter'], 
 +                                                           convergence_iter=self.AffinityPropagation['convergence_iter'],
 +                                                           copy=self.AffinityPropagation['copy'], 
 +                                                           preference=self.AffinityPropagation['preference'],
 +                                                           affinity=self.AffinityPropagation['affinity'], 
 +                                                           verbose=self.AffinityPropagation['verbose'])
 +        clustering_algorithms = [dbscan,affinity_propagation]  
 +        clustering_names = ['DBSCAN','AffinityPropagation']
 +        for name, algorithm in zip(clustering_names, clustering_algorithms):
 +            self.suanfa[name]={}
 +            t0 = time.time()
 +            algorithm.fit(dataset)
 +            t1 = time.time()
 +            self.suanfa[name]['time']=t1-t0
 +            if hasattr(algorithm, 'labels_'):
 +                y_pred = algorithm.labels_.astype(np.int)
 +            else:
 +                y_pred = algorithm.predict(dataset)
 +            l=len(set(y_pred))
 +            y_pred=np.array([y_pred[l]  if y_pred[l]!=-1 else l-1 for l in range(len(y_pred))])
 +            self.suanfa[name]['y_pred']=y_pred
 +
 +            if hasattr(algorithm, 'cluster_centers_'):
 +                centers = algorithm.cluster_centers_
 +                self.suanfa[name]['centroids']=centers
 +            else:
 +                #如果算法没有centers_属性，则采用聚类数求平均值方法。
 +                l=len(set(self.suanfa[name]['y_pred']))
 +                le=set(self.suanfa[name]['y_pred'])
 +                p=[];c=np.zeros((l,self.dataset.shape[1]))
 +                t=0
 +                for j in le:
 +                    p=np.nonzero(self.suanfa[name]['y_pred']==j)[0]
 +                    data=np.mat(self.dataset)[p,:]
 +                    if data.shape[0]!=1:
 +                        c[t]=np.mean(data,axis=0)
 +                    else:
 +                        c[t]=data
 +                    t=t+1
 +                self.suanfa[name]['centroids']=np.array(c)
 +
 +        key=list(self.suanfa.keys())
 +        self.keys=key
 +        suanfa1= copy.deepcopy(self.suanfa)   #suanfa1储存pca后的聚类中心
 +
 +        H={}  #用于储存每个聚类的半径值(平均半径)
 +        Max={} #最大距离
 +        Min={}#最小距离
 +        
 +        key=['DBSCAN','AffinityPropagation']
 +        num1=len(self.suanfa['DBSCAN']['centroids'])
 +        num2=len(self.suanfa['AffinityPropagation']['centroids'])
 +        for j in range(2):
 +            H[key[j]]=[]
 +            Max[key[j]]=[]
 +            Min[key[j]]=[]
 +            if key[j]=='DBSCAN' :
 +                df=pd.concat([dataset,pd.DataFrame(self.suanfa['DBSCAN']['centroids'])]) 
 +                redu=PCA(n_components=2).fit_transform(df) 
 +                suanfa1[key[j]]['centroids']=redu[-num1:,:] 
 +
 +                h=self.average_special(df[:-num1],j,self.suanfa['DBSCAN']['y_pred'])  #计算平均距离，j是算法索引，num1是聚类数
 +                H[key[j]].append(h)
 +
 +                M1,M0=self.maxRminR1_special(df[:-num1],j,self.suanfa['DBSCAN']['y_pred'])
 +                Max[key[j]].append(M1)
 +                Min[key[j]].append(M0)
 +            else:
 +                df=pd.concat([dataset,pd.DataFrame(self.suanfa['AffinityPropagation']['centroids'])]) 
 +                redu=PCA(n_components=2).fit_transform(df) 
 +                suanfa1[key[j]]['centroids']=redu[-num2:,:] 
 +
 +                h=self.average_special(df[:-num2],j,self.suanfa['AffinityPropagation']['y_pred'])  #计算平均距离，j是算法索引，num2是聚类数
 +                H[key[j]].append(h)
 +                #print(H[key[j]])
 +                
 +                M1,M0=self.maxRminR1_special(df[:-num2],j,self.suanfa['AffinityPropagation']['y_pred'])
 +                Max[key[j]].append(M1)
 +                Min[key[j]].append(M0)
 +                #print(Min[key[j]])
 +        self.suanfa1=suanfa1
 +        self.plot_Circle_special(H,Max,Min) #绘图函数，聚类数i  
 +        self.Jun_level()
 +        
 +    def average_special(self,df,i,y_pred): 
 +        key=['DBSCAN','AffinityPropagation']
 +        if key[i]=='DBSCAN' or key[i]=='AffinityPropagation':
 +            ds=[] #平均距离
 +            count=0   #用于遍历聚类中心
 +            p=list(set(y_pred))
 +            for j in p:
 +                #开始计算平均距离
 +                lei=np.nonzero(self.suanfa[key[i]]['y_pred']==j)[0]
 +                d=0
 +                for k in lei:
 +                    d=d+self.enlid(self.suanfa[key[i]]['centroids'][count],df.iloc[k,:])
 +                count=count+1
 +                ds.append(d/len(lei))
 +        h=ds
 +        return h  
 +    
 +    def maxRminR1_special(self,df,i,y_pred): 
 +        h1=[]
 +        h0=[]
 +        key=['DBSCAN','AffinityPropagation']
 +        if key[i]=='DBSCAN' or key[i]=='AffinityPropagation':
 +            dm=[] #最大距离
 +            di=[]#最小距离
 +            p=list(set(y_pred))  #聚类的标号
 +            count=0
 +            for j in p:
 +                #开始计算平均距离
 +                lei=np.nonzero(self.suanfa[self.key[i]]['y_pred']==j)[0]
 +                maxd=0
 +                minr=np.inf
 +                for k in lei:
 +                    d=self.enlid(self.suanfa[key[i]]['centroids'][count],df.iloc[k,:])
 +                    
 +                    if maxd<d:maxd=d
 +                    if minr>d:minr=d
 +                count+=1
 +                dm.append(maxd)
 +                di.append(minr)
 +            h1=dm
 +            h0=di
 +        return h1,h0
 +    
 +    def Drawnet(self):
 +        '''connectivity 的计算方法，可以用于AgglomerativeClustering以及ward'''
 +        #connectivity = kneighbors_graph(dataset, n_neighbors=7, include_self=False)
 +        #connectivity = 0.5 * (connectivity + connectivity.T)
 +                     
 +        two_means = cluster.MiniBatchKMeans(n_clusters=self.cluster_num, init=self.KMeans['init'], max_iter=self.KMeans['max_iter'], 
 +                                            batch_size=self.KMeans['batch_size'],verbose=self.KMeans['verbose'], 
 +                                            compute_labels=self.KMeans['compute_labels'], 
 +                                            random_state=self.KMeans['random_state'], tol=self.KMeans['tol'], 
 +                                            max_no_improvement=self.KMeans['max_no_improvement'], init_size=self.KMeans['init_size'], 
 +                                            n_init=self.KMeans['n_init'], reassignment_ratio=self.KMeans['reassignment_ratio'])
 +                     
 +        ward = cluster.AgglomerativeClustering(n_clusters=self.cluster_num, affinity=self.ward['affinity'], 
 +                                               connectivity=self.ward['connectivity'], 
 +                                               compute_full_tree=self.ward['compute_full_tree'], 
 +                                               linkage=self.ward['linkage'], pooling_func=self.ward['pooling_func'])
 +        spectral = cluster.SpectralClustering(n_clusters=self.cluster_num, eigen_solver=self.SpectralClustering['eigen_solver'], 
 +                                              random_state=self.SpectralClustering['random_state'], 
 +                                              n_init=self.SpectralClustering['n_init'], gamma=self.SpectralClustering['gamma'], 
 +                                              affinity=self.SpectralClustering['affinity'], n_neighbors=self.SpectralClustering['n_neighbors'], 
 +                                              eigen_tol=self.SpectralClustering['eigen_tol'], 
 +                                              assign_labels=self.SpectralClustering['assign_labels'], degree=self.SpectralClustering['degree'], 
 +                                              coef0=self.SpectralClustering['coef0'], kernel_params=self.SpectralClustering['kernel_params'], 
 +                                              n_jobs=self.SpectralClustering['n_jobs'])
 +
 +        average_linkage = cluster.AgglomerativeClustering(n_clusters=self.cluster_num, 
 +                                               affinity=self.AgglomerativeClustering['affinity'], 
 +                                               connectivity=self.AgglomerativeClustering['connectivity'], 
 +                                               compute_full_tree=self.AgglomerativeClustering['compute_full_tree'], 
 +                                               linkage=self.AgglomerativeClustering['linkage'], 
 +                                               pooling_func=self.AgglomerativeClustering['pooling_func'])
 +        
 +        birch = cluster.Birch(threshold=self.Birch['threshold'], branching_factor=self.Birch['branching_factor'], 
 +                              n_clusters=self.Birch['n_clusters'], compute_labels=self.Birch['compute_labels'],
 +                              copy=self.Birch['copy'])
 +        
 +        clustering_algorithms = [two_means, spectral, ward,average_linkage,birch]
 +        
 +        clustering_names = [
 +        'MiniBatchKMeans', 
 +        'SpectralClustering', 'Ward', 'AgglomerativeClustering',
 +        'Birch']
 +        suanfa={}
 +        
 +        for name, algorithm in zip(clustering_names, clustering_algorithms):
 +            suanfa[name]={}
 +            t0 = time.time()
 +            algorithm.fit(dataset)
 +            t1 = time.time()
 +            suanfa[name]['time']=t1-t0
 +            if hasattr(algorithm, 'labels_'):
 +                y_pred = algorithm.labels_.astype(np.int)
 +                #print(y_pred)
 +            else:
 +                y_pred = algorithm.predict(dataset)
 +                #print(y_pred)
 +            l=len(set(y_pred))
 +            y_pred=np.array([y_pred[l]  if y_pred[l]!=-1 else l-1 for l in range(len(y_pred))])
 +            suanfa[name]['y_pred']=y_pred
 +
 +            if hasattr(algorithm, 'cluster_centers_'):
 +                centers = algorithm.cluster_centers_
 +                suanfa[name]['centroids']=centers
 +            else:
 +                #如果算法没有centers_属性，则采用聚类数求平均值方法。
 +                p=[];c=np.zeros((self.cluster_num,self.dataset.shape[1]))
 +                for j in range(self.cluster_num):
 +                    p=np.nonzero(suanfa[name]['y_pred']==j)[0]
 +                    if len(p)==0:
 +                        print("算法本身不允许聚类数达到如此之大，因为某些聚类中心没有样本。")
 +                        print("第%d个聚类中心没有聚类到样本点（聚类数从1开始）"%(j+1))
 +                        print("请重新选择聚类数")
 +                    data=np.mat(dataset)[p,:]
 +                    c[j]=np.mean(data,axis=0)
 +                suanfa[name]['centroids']=c
 +
 +        key=list(suanfa.keys())
 +        self.key=key
 +        self.suanfa=suanfa
 +        suanfa1= copy.deepcopy(suanfa)   #suanfa1储存pca后的聚类中心
 +
 +        H={}  #用于储存每个聚类的半径值(平均半径)
 +        Max={} #最大距离
 +        Min={}#最小距离
 +        for j in range(5):
 +            H[key[j]]=[]
 +            Max[key[j]]=[]
 +            Min[key[j]]=[]
 +            if key[j]!='DBSCAN' and key[j]!='AffinityPropagation':
 +                df=pd.concat([dataset,pd.DataFrame(suanfa[list(suanfa.keys())[j]]['centroids'])])
 +                redu=PCA(n_components=2).fit_transform(df) 
 +                suanfa1[key[j]]['centroids']=redu[-self.cluster_num:,:] 
 +                #print(redu[-i:,:] )
 +                #print(list(suanfa.keys())[j])
 +                #print(df[:-self.cluster_num].shape, suanfa[keys[j]]['centroids'].shape,suanfa1[keys[j]]['centroids'].shape)
 +
 +                h=self.average(df[:-self.cluster_num],j,self.cluster_num)  #计算平均距离，j是算法，i是聚类数
 +                H[key[j]].append(h)
 +
 +                M1,M0=self.maxRminR1(df[:-self.cluster_num],j,self.cluster_num)
 +                Max[key[j]].append(M1)
 +                Min[key[j]].append(M0)
 +        self.suanfa1=suanfa1
 +        self.plot_Circle(self.cluster_num,H,Max,Min) #绘图函数，聚类数i  
 +        self.special_algorithm()
 +        #self.Jun_level();
 +        
 +import random
 +data = load_iris()
 +dataset=pd.DataFrame(data['data'])
 +
 +d=DrawCluster(dataset,3)
 +d.Drawnet()
 +
 +x=len(dataset)
 +for i in [10,20,30,40,50,x]:
 +    dataset=pd.DataFrame(data['data'])
 +    dataindex=random.sample(range(x),i)
 +    #print(dataindex,i)
 +    dataset=dataset.iloc[dataindex,:]
 +    #print(dataset)
 +    d=DrawCluster(dataset,3)
 +    d.Drawnet()
