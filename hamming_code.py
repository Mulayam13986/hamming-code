def encoder(message, extra_bit):
    message = list(message)
    mess_len = len(message)
    for i in range(mess_len):
        message[i] = int(message[i])
    parity_bit_cnt = 0
    while(True):
        if (2**(parity_bit_cnt) >= mess_len+parity_bit_cnt+1):
            break
        parity_bit_cnt+=1
    encoded_len = mess_len + parity_bit_cnt + 1

    list1 = [0]*(encoded_len) 
    a = {}
    for i in range(parity_bit_cnt):
        idx = 2**i
        list1[idx] = -1

    idx = 1
    for i in range(mess_len):

        while(list1[idx] == -1) : 
            list1[idx] = 0
            idx+=1 
        list1[idx] = message[i] 
        idx+=1 
    
    for i in range(parity_bit_cnt):
        idx  = 2**i
        val = 0 

        j = idx  
        while(j < encoded_len):
        
            temp = 0 
            while(j < encoded_len and temp < idx):
                if (j != idx):
                    val^= list1[j] 
                temp+=1
                j+=1
        
            j+= idx 
        list1[idx] = val 
    complete_xor = 0 
    for i in range(1,encoded_len):
        complete_xor ^= list1[i] 
    list1[0] = complete_xor
    for i in range(len(list1)):
        list1[i] = str(list1[i])
    if (extra_bit):
        return "".join(list1)
    return "".join(list1[1:])



# print(encoder("1111" , 0))



def no_error(vis,n,codeword):
    mess = ""

    for i in range(1,n+1):
        if (not vis[i]):
            mess += str(codeword[i])
    return [mess,0,0]


def single_error(parity_bit_cnt,expected_parity_bits,given_parity_values,codeword,n,vis,extra_bit): 
    l1 = []

    for i in range(parity_bit_cnt):
        if (expected_parity_bits[i] != given_parity_values[i]):
            l1.append(1)
        else:
            l1.append(0)
    l1 = l1[::-1] 

    error_bit = 0
    for i in range(len(l1)):
        error_bit = 2*error_bit + l1[i] 
    mess = ""
    for i in range(1,n+1):
        if(vis[i]) :
            continue
        if (i== error_bit):
            mess+= str(int(not codeword[i]))
        else :
            mess+= str(codeword[i]) 
    error_bit_idx = error_bit 
    if (extra_bit) :
        error_bit_idx = error_bit+1 
    else : 
        error_bit_idx = error_bit
    return [mess,1,error_bit_idx]
def decoder(codeword,extra_bit):
    if(not extra_bit):
       codeword = '0' + codeword 
    codeword = list(codeword)
    mess_len = len(codeword)
    n= mess_len - 1
    for i in range(mess_len):
        codeword[i] = int(codeword[i])
    parity_bit_cnt = 0

    while(True):
        if (2**parity_bit_cnt >= n+1):
            break
        parity_bit_cnt+=1
        

    expected_parity_bits = [0]*parity_bit_cnt
    parity_bit_idx = []
    given_parity_values = [] 
    vis = [0]*(n+1)
    for i in range(parity_bit_cnt): 
        parity_bit_idx.append(2**i) 
        given_parity_values.append(codeword[2**i]) 
        vis[2**i]=1 
    
    for i in range(parity_bit_cnt):
        idx  = 2**i
        val = 0 

        j = idx  
        while(j <= n):

            temp = 0 
            while(j <= n and temp < idx):
                if (j != idx):
                    val^= codeword[j] 
                temp+=1
                j+=1
            
            j+= idx
        expected_parity_bits[i] =  val 
    

    if(not extra_bit): 
        check = 1
        for i in range(parity_bit_cnt):

            if (expected_parity_bits[i] != given_parity_values[i]):

                check = 0
                break 
        
        if (check) :
            
            mess =  no_error(vis,n,codeword)
            return mess 
        else :
            mess = single_error(parity_bit_cnt,expected_parity_bits,given_parity_values,codeword,n,vis,extra_bit)
            return mess 
    
    else:
        overall_par = 0
        for i in range(1,mess_len):
            overall_par^= codeword[i] 
        p = 1
        if(overall_par != codeword[0]):
            p = 0 
        
        
        check = 1
        for i in range(parity_bit_cnt):

            if (expected_parity_bits[i] != given_parity_values[i]):

                check = 0
                break 
        
        if(p==1 and check == 1): 
            return no_error(vis,n,codeword)
        elif (p==1 and check == 0):
            return ["double error detected but can not be corrected",2,0]
        elif (p==0):
            return single_error(parity_bit_cnt,expected_parity_bits,given_parity_values,codeword,n,vis,extra_bit)
        
        return ["error",-1]



# print(decoder("0011111" , 0))

import numpy as np
def error_simulation(codeword): 
    r = np.random.rand()
    codeword = list(codeword)
    n = len(codeword)
    if (r <= 0.4) :
        return "".join(codeword)
    elif (r <= 0.9): 
        n1 = np.random.randint(0,n) 

        codeword[n1] = str(int(not codeword[n1])) 
    else:
        n1 = np.random.randint(0,n) 
        n2 = n1
        while(True):
           if(n2 != n1):
               break
           n2 = np.random.randint(0,n) 
        codeword[n1] = str(int(not codeword[n1])) 
        codeword[n2] = str(int(not codeword[n2])) 
    return "".join(codeword)


    