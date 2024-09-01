import pygame,math
import models,converter,sorter
import numpy as np

pygame.init()

win=pygame.display.set_mode((720,405))
pygame.display.set_caption(".OBJ Viewer")
clock=pygame.time.Clock()
run=True

def proj(x,y,z,w,h,theta):
    xn=(w/2)*(x/z)*math.tan(math.radians(theta/2))
    yn=(w/2)*(y/z)*math.tan(math.radians(theta/2))
    xn+=w/2
    yn+=h/2

    return xn,yn


def draw_obj(obj,pos,anglee,w,h,theta,win,color,light):
    x,y,z=pos
    ax,ay,az=anglee
    rotated_model=[]
    sorted_model=[]
    
    for triangle in obj:
        v=0
        for vertex in triangle:
            #rotation
            x1,y1,z1=rotx((vertex[0],vertex[1],vertex[2]),ax)
            x2,y2,z2=roty((x1,y1,z1),ay)
            vrx,vry,vrz=rotz((x2,y2,z2),az)
            
            v+=1

            if v==1:
                a=vrx,vry,vrz
            if v==2:
                b=vrx,vry,vrz
            if v==3:
                c=vrx,vry,vrz
                rotated_model.append([ a,b,c ])
    
    sorted_model = sorter.sort_triangles(rotated_model)
    #sorted_model = rotated_model
    
    for triangle in sorted_model:
        v=0
        for vertex in triangle:
            #projection values
            vrx,vry,vrz=vertex
            xc,yc=proj(x+vrx,y+vry,z+vrz,w,h,theta)

            #normal and draw
            if v==0:
                a=xc,yc
                a3=x+vrx,y+vry,z+vrz
            if v==1:
                b=xc,yc
                b3=x+vrx,y+vry,z+vrz
            if v==2:
                c=xc,yc
                c3=x+vrx,y+vry,z+vrz

                
                line1=[  b3[0]-a3[0],b3[1]-a3[1],b3[2]-a3[2]  ]
                line2=[  c3[0]-a3[0],c3[1]-a3[1],c3[2]-a3[2]  ]

                nx,ny,nz=np.cross(line1,line2)
                nl=(nx**2 + ny**2 +nz**2)**0.5
                
                if not(nl==0):
                    nx/=nl
                    ny/=nl
                    nz/=nl
                else:
                    print("zero normal !!!")

                
                if (nx*a3[0])+(ny*a3[1])+(nz*a3[2])<0:
                    '''
                    pygame.draw.line(win,((255,0,0)),a,b,5)
                    pygame.draw.line(win,((0,255,0)),b,c,5)
                    pygame.draw.line(win,((0,0,255)),c,a,5)
                    '''

                    lx,ly,lz=light
                    lsize=(lx**2 + ly**2 +lz**2)**0.5

                    lx/=lsize
                    ly/=lsize
                    lz/=lsize

                    light=lx,ly,lz
                    
                    shade=(nx*light[0])+(ny*light[1])+(nz*light[2])
                    if shade<0:
                        shade=0
                    shade=1-shade
                    #shade=1
                    pygame.draw.polygon(win,(color[0]*shade,color[1]*shade,color[2]*shade),[a,b,c])
                    
            v+=1
            
def rotx(pos,rot):
    x,y,z=pos

    x_=x
    y_=(y*math.cos(rot))-(z*math.sin(rot))
    z_=(y*math.sin(rot))+(z*math.cos(rot))

    return x_,y_,z_

def roty(pos,rot):
    x,y,z=pos

    x_=(x*math.cos(rot))+(z*math.sin(rot))
    y_=y
    z_=(z*math.cos(rot))-(x*math.sin(rot))

    return x_,y_,z_

def rotz(pos,rot):
    x,y,z=pos

    x_=(x*math.cos(rot))-(y*math.sin(rot))
    y_=(x*math.sin(rot))+(y*math.cos(rot))
    z_=z

    return x_,y_,z_



monkey=converter.convert("monky.obj")
aaa=0
print(len(monkey))


while run:
    win.fill((0,0,0))
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run=False
    aaa+=0.025

    
    draw_obj(monkey,(0,0,5),(0,aaa,aaa),720,405,90,win,(150,150,150),(10,10,-2))
        
    pygame.display.update()
    clock.tick(60)
    print(clock.get_fps())
    

pygame.quit()
