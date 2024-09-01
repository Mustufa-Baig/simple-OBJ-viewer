def convert(fyle):
    with open(fyle,'r') as f:
        f2=f.read()
        f3=f2.split("\n")
        verticies=[]
        faces=[]

        for line in f3:
            try:
                if line[0]=='v':
                    line2=line.split(" ")
                    x,y,z=line2[1],line2[2],line2[3]
                    verticies.append([float(x),float(y),float(z)])
            except:
                pass
            
        for line in f3:
            try:
                if line[0]=='f':
                    line2=line.split(" ")
                    v1,v2,v3=line2[1],line2[2],line2[3]
                    faces.append([ verticies[(int(v1) -1)] ,verticies[(int(v2) -1)] ,verticies[(int(v3) -1)] ])
            except:
                pass
    
    return faces


