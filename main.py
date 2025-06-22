from graphics import Canvas
import time
import random
    
CANVAS_WIDTH = 420
CANVAS_HEIGHT = 600

def ice_climber_set(canvas,x,y,color):
    return canvas.create_rectangle(
            x, y, x+20, y+20, color)

def brick_set(canvas,bx,by,color,outline):
    return canvas.create_rectangle(
            bx, by, bx+30, by+10, color,outline)

def cloud_set(canvas,cx,cy,color):
    return canvas.create_rectangle(
            cx, cy, cx+40, cy+10, color)

def enemy_set(canvas,ex,ey,color):
    return canvas.create_rectangle(
            ex, ey, ex+20, ey+20, color)

def goal_set(canvas,gx,gy,color):
    return canvas.create_rectangle(
            gx, gy, gx+20, gy+20, color)


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

#goal_set
    gx=random.randint(0,CANVAS_WIDTH-20)
    gy=random.randint(0,50)
    goal=goal_set(canvas,gx,gy,"pink")

#brick fixed
    b_column=int(CANVAS_WIDTH//30)
    b_row=int((CANVAS_HEIGHT//100)-1)
    e_list=[] 
    b_list=[]
    for y in range(1,b_row+1): 
        by=y*100
        bx_list=[]
        for x in range(b_column):
            if random.random()<0.8:
                bx=x*30
                brick=brick_set(canvas, bx,by,"brown","white")
                bx_list.append(bx)
                b_list.append(brick)

#enemy　move(1)(stand on brick)                
        if bx_list:
            ex1=random.choice(bx_list)
            ey=by-20
            e_vx=10
            enemy_1=enemy_set(canvas,ex1,ey,"orange")
            e_list.append([enemy_1, ex1, ey, e_vx])
            if random.random()<0.5:
                bx_list.remove(ex1)
                ex2=random.choice(bx_list)
                enemy_2=enemy_set(canvas,ex2,ey,"orange")
                e_list.append([enemy_2, ex2, ey, e_vx])
           
#cloud move(1)
    cx=100
    cy=350
    c_vx=10
    cloud_1=cloud_set(canvas, cx, cy,"cyan")
    cloud_2=cloud_set(canvas, cx, 130,"cyan")


#ice_climber
    x=20
    y=580
    ic=ice_climber_set(canvas,x,y,"blue")
    vx=0
    vy=0
    jump_v=-40
    g=5
    while True:
        time.sleep(0.1)
        ic_direction = canvas.get_last_key_press()
        if ic_direction == "ArrowLeft":
            vx=-5
        if ic_direction == "ArrowRight":
            vx=5
        if ic_direction == "ArrowUp":
            vy=jump_v

        x=x+vx
        vy=vy+g
        y=y+vy

        if y > CANVAS_HEIGHT-20:
            y = CANVAS_HEIGHT-20
            vy=0
        if x < 0:
            x=0
            vx=0
        if x > CANVAS_WIDTH-20:
            x=CANVAS_WIDTH-20
            vx=0  
        
#break_brick
        colliding_ib = canvas.find_overlapping(x, y , x+20, y+20)
        for i in colliding_ib:
            coords = canvas.coords(i)
            if i in b_list:
                if vy>0:
                    y=coords[1]-20
                    vy=0
                if vy<0:
                    canvas.delete(i)
                    b_list.remove(i)
                    vy=-vy
                    
        canvas.moveto(ic,x,y)

##cloud move(2)
        cx=cx+c_vx
        canvas.moveto(cloud_1,cx,cy)
        canvas.moveto(cloud_2,cx,130)
        colliding_ic = canvas.find_overlapping(x, y , x+20, y+20)
        if cx <= 0 or cx+40 >= CANVAS_WIDTH:
            c_vx=-c_vx
        if cloud_1 in colliding_ic:
            vy=-vy
        if cloud_2 in colliding_ic:
            vy=-vy

##enemy move(2) -會有滑出去的現象
        new_e_list = []
        for e in range(len(e_list)):
            enemy, ex, ey, e_vx = e_list[e]
            ex=ex+e_vx
            canvas.moveto(enemy,ex,ey)
            colliding_eb = canvas.find_overlapping(ex, ey , ex+10, ey+21)
            colliding_ie = canvas.find_overlapping(x, y, x+20, y+20)
            on_brick = any(obj in b_list for obj in colliding_eb)
            if not on_brick:
                e_vx = -e_vx
                ex=ex+e_vx
            if ex <= 0 or ex+20 >= CANVAS_WIDTH:
                e_vx=-e_vx
                ex=ex+e_vx 
            if enemy in colliding_ie:
                if y>ey:
                    canvas.delete(enemy)
                else:
                    return print("lose")
            new_e_list.append([enemy, ex, ey, e_vx])
        e_list = new_e_list
            
#goal
        colliding_ig = canvas.find_overlapping(x, y , x+20, y+20)
        if goal in colliding_ig:
            print("win")
            break

       

if __name__ == '__main__':
    main()
