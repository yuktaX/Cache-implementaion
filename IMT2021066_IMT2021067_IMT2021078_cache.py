from cmath import log
import sys
import math

def hex_to_binary(x):       #func to covert hex address to 32-bit binary address
        a=bin(int(x,base=16))
        b=a[2:len(a)]
        return ('0'*(32-len(b))+b)

#This code is common for all parts of the question. For changing cache size, block size and number of ways they have been kept as variables entered by user on running the program

#taking number of ways, cache size and block size as input
n=int(input('Enter no of ways: '))      
size=int(input('Enter cache size in kB: '))
block=int(input('Enter block size in bytes: '))
lines = int((size * 1024)/ (block * n))

#calculating the index, offset and tag bits
index_bits=int(math.log(lines,2))
offset_bits=int(math.log(block,2))
tag_bits=32-index_bits-offset_bits

#list containing trace files
files=['gcc.trace','gzip.trace','mcf.trace','swim.trace','twolf.trace']

print(str(n)+' way set associatice cache')
print(str(size)+' = cache size(kB)  ,'+str(block)+' = block size(bytes)  ,' + str(lines) +' = lines ')

#iterate through the trace files and calculate the hit count and miss count for each of them
for f in range (5):
    #open the trace file to be read
    sys.stdin = open(files[f], 'r')

    #initialize hit count and miss count variables
    hit_count=0
    miss_count=0

    #create the cache structure and initialize the data to 0
    cache1=[[[0,0,0] for x in range(n)] for i in range(lines)]
    #each cache block has [valid bit,tag,LRU] 

    while(1):
        try:
            initial_address=input()
        except EOFError as end:     #terminating condition when end of reading input is reached
            print('\n')
            print('*****',files[f],'*****')
            break

        
        address= hex_to_binary(initial_address[4:12]) #slicing address to get tag and index bits
        tag = address[0:tag_bits]
        index = int(address[tag_bits:tag_bits+index_bits],2)
        offset = address[tag_bits+index_bits:32]

        
        flg = 0

        for way in range(n):
            if(cache1[index][way][1]==(tag) and cache1[index][way][0]==1):  #cond to check for cache hit
                hit_count += 1                                              #increment hit count
                flg = 1
                cache1[index][way][2] = 0                                   #make the LRU value of the current block 0
                for i in range(n):                                          #and increase it for the other blocks of the line
                    if i != way :
                        cache1[index][i][2] += 1

            
        #implementation of cache miss along with LRU 
        if(flg==0): 
            miss_count+=1
            way_replace = 0
            max_lru = -1
            for i in range (n):                                             #find the maximum value of LRU in the current line
                if (cache1[index][i][2] > max_lru):
                    max_lru = cache1[index][i][2]
                    
            for way in range(n):                                            #find the corresponding block that has the maximum LRU
                if cache1[index][way][2] == max_lru:
                    way_replace = way

            cache1[index][way_replace][0] = 1                               #replace the data of the above found block with new data
            cache1[index][way_replace][1] = tag
            cache1[index][way_replace][2] = 0

            for i in range(n):                                              #increase the LRU value of the other blocks in the line
                    if i != way_replace :
                        cache1[index][i][2] += 1

    print('Hit count-> ',hit_count,end='   ')
    print('Hit rate->', (hit_count/(hit_count+miss_count))*100,'%')
    print('Miss count-> ',miss_count,end='   ')
    print('Miss rate->', (miss_count/(hit_count+miss_count))*100,'%')
    print('Hits/Misses', hit_count/miss_count)
    print('-----------------------------------------------------------------')