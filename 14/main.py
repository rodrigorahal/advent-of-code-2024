import fileinput
import re
import time


def parse():
    robots = []
    pattern = r"-?\b\d+\b"
    for line in fileinput.input():
        matches = re.findall(pattern, line.strip())
        robots.append([int(m) for m in matches])
    return robots


def tick(H, W, robot):
    px, py, vx, vy = robot
    npx, npy = px + vx, py + vy
    if npx < 0:
        npx = W + npx
    elif npx >= W:
        npx = npx - W
    if npy < 0:
        npy = H + npy
    elif npy >= H:
        npy = npy - H
    return [npx, npy, vx, vy]


def simulate(H, W, robots, times=100):
    curr = robots
    for i in range(times):
        updated = [tick(H, W, robot) for robot in curr]
        curr = updated
    return curr


def quadrants(H, W, robots):
    q1, q2, q3, q4 = 0, 0, 0, 0

    for robot in robots:
        px, py, vx, vy = robot

        if 0 <= px < W // 2 and 0 <= py < H // 2:
            q1 += 1
            continue
        if W // 2 < px <= W and 0 <= py < H // 2:
            q2 += 1
            continue
        if 0 <= px < W // 2 and H // 2 < py <= H:
            q3 += 1
            continue
        if W // 2 < px <= W and H // 2 < py <= H:
            q4 += 1
            continue
    return q1 * q2 * q3 * q4


def display(H, W, robots):
    S = set([(px, py) for px, py, _, _ in robots])
    for y in range(H + 1):
        row = []
        for x in range(W + 1):
            if (x, y) in S:
                row.append(".")
            else:
                row.append(" ")
        print("".join(row))
    print()


def search(H, W, robots, times=7000):
    curr = robots
    for i in range(times):
        updated = [tick(H, W, robot) for robot in curr]
        # added after visual inspection
        if i == 6532 - 1:
            display(H, W, updated)
            return 6532
        curr = updated
    return -1


def main():
    H, W = 103, 101
    robots = parse()
    print(f"Part 1: {quadrants(H, W, simulate(H, W, robots))}")
    print(f"Part 2: {search(H, W, robots, times=7000)}")


if __name__ == "__main__":
    main()

"""
                        ...............................                                               
               .        .                             .                                               
                        .                             .                        .                      
              .         .                             .                                               
                        .                             .                                               
                        .              .              .                          .   .                
                        .             ...             .                      .                        
      .                 .            .....            .                                               
                        .           .......           .                   .                           
       .            .   .          .........          .                                             . 
                        .            .....            .                                               
 .                      .           .......           .                                   .           
                        .          .........          .                     .                         
                        .         ...........         .                                               
                        .        .............        .                                               
                        .          .........          .                                               
      .                 .         ...........         .                                    .        . 
                        .        .............        .                                               
           .            .       ...............       .                                               
                        .      .................      .                                               
                        .        .............        .                                               
                        .       ...............       .                                               
                        .      .................      .  .                                            
                        .     ...................     .                                           .   
                        .    .....................    .                  .  .                         
                        .             ...             .                                               
                        .             ...             .                                               
                        .             ...             .                                        .      
 .                      .                             .  .                                            
    .                   .                             .            .                                  
      .     .           .                             .                       .                       
                        .                             .                              .                
                        ...............................                 .                             
                                                                        .                             
"""
