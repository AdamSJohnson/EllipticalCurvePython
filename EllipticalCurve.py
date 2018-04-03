import random
def gcd(a,b):
    #Super fast super good
    a,b=(b,a) if a<b else (a,b)
    while b:
        a,b=b,a%b
    return a

def egcd(a,b):
    #
    # Extended Euclidean Algorithm
    # returns x, y, gcd(a,b) such that ax + by = gcd(a,b)
    #

    #initialize our x vals
    u, u1 = 1, 0
    #initialize our y vals
    v, v1 = 0, 1

    #keep going until we get a remainder of 0
    while b:
        #get our integer quotient 
        q = a // b
        #update our x and y vals
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        #replace a with b and b with a%b
        a, b = b, a - q * b
    return u, v, a

def isprime(n):
    #check if n is prime
    #pick 'a' such that 'a' is an element of {2,..,n-1} 100 times
    # probably too much checking  ¯\_(ツ)_/¯
    for q in range(100):
        #slick lets pick a random a in our range
        a = random.randint(2,n-1)
        #even slicker is if this fn evaluates to 1
        if pow(a, n - 1, n) != 1:
            #awman tfw not prime
            return 0
    #good enough this is probably prime
    return 1

#I wanted threads and this is what I had to do
#    Deal
#Wi
#   th     i
#          t
def prime_maker(n_bits):
    padder = 1 << n_bits - 1
    p = random.getrandbits(n_bits)

    # p might not have n bits so we just want to make sure the most signigicant bit is a 1
    # bit-wiseOR p with (1 << n_bits - 1)
    # bit-wiseOR p with 1 to ensure oddness 
    p = p | padder
    p = p | 1

    #keep generating primes until we win
    while not isprime(p):
        p = random.getrandbits(n_bits)
        # p might not have n bits so we just want to make sure the most signigicant bit is a 1
        # bit-wiseOR p with (1 << n_bits - 1)
        # bit-wiseOR p with 1
        p = p | padder
        p = p | 1
    return p

#simple function to get back a tuple of A, B, and q values
def build_ec(a=1, b=1, n_bits=4):
    #check our discriminant
    disc = 4 * pow(a, 3) + 27 * pow(b, 2)
    if disc == 0:
        return (-1,-1,-1)
    #our prime q should be n_bits and q mod 4 should equal 3 for this system
    q = prime_maker(n_bits)
    while q %  4 == 1:
        q = prime_maker(n_bits)
    #generate a prime that q mod 4 = 3
    return (a, b, q)

def generate_field(ec = (1,1,11)):
    ret_field = []
    leg = (ec[2]-1)/2
    sec = (ec[2]+1)/4
    for i in range(ec[2]):
        a = (pow(i, 3) + ec[0] * i + ec[1]) % ec[2]
        if (pow(a, leg) % ec[2]) == 1:
            v = (pow(a, sec) % ec[2])
            tup = (i, int(v))
            tup2 = (i, int(ec[2] - v))
            ret_field.append(tup)
            ret_field.append(tup2)
    return ret_field

def point_addition(a=(-1,-1), b=(-1,-1), ec = (-1,-1,-1)):
    #call must pass new values
    if a == (-1,-1) or b == (-1,1) or ec[2] == -1:
        print('change em')
        return 0
    q = ec[2]
    #make sure we are adding points in the field
    if a == 0:
        return b
    if b == 0:
        return a
    if True:
        #print('good')
        #case 1 a.x != b.x
        if a[0] != b[0]:
            #print('not equal points')
            #different point addition
            #get y and do correct negative modulus
            y_comp = a[1] - b[1]
            
            #get x and do correct negative modulus
            x_comp = a[0]-b[0]
            
            y_comp = y_comp % q
            x_comp = x_comp % q

            #calculate m 
            m =  y_comp * egcd(q, x_comp)[1] 
            m = m % q
            #solve the lines
            x_r = pow(m, 2) - (a[0] + b[0])
            
            x_r = x_r % q
            y_r = a[1] + m * (x_r - a[0])
            
            y_r = y_r % q

            
            return (x_r, q - y_r)
            
        #point doubling case
        if a == b:
            #print('equal points')
            #calculat the x part of m
            m_x = 3*pow(a[0], 2) + ec[0]
            
            #correct positive mod
            m_x = m_x % q
            #print('a')
            #calculate the y inverse
            m_y = 2 * a[1]
            
            #print('b_1')
            m_y = m_y % q
            m_y = egcd(q, m_y)[1]
            #print('b_2')
            #get the full m
            m = m_x * m_y
            m = m % q

            x_r = pow(m, 2) - 2 * a[0]
            
            #print('c')  
            x_r = x_r % q

            y_r = a[1] + m * (x_r - a[0])

            #print('d') 
            y_r = y_r % q
            return (x_r, q - y_r)
    # if we end up here we are in the negative case p + (-p) = infinity point
    return 0

def multiply_point(n=-1, p=(-1,-1),  ec=(-1,-1,-1)):
    if n < 1:
        return 0
    if p == (-1,-1) or  ec[2] == -1:
        return 0
    Q = 0
    R = p
    while n > 0:
        if n & 1 == 1:
            Q = point_addition(a=Q, b=R, ec=ec)
        R = point_addition(a=R, b=R, ec=ec)
        n =  n >> 1

    return Q

def secondmain():
    file = open('elgamal.keys', 'r')
    encrypted = open('elgamal_cipher_suny.txt','r')
    ciphers = []
    for x in encrypted:
        x.replace('\n','')
        x.replace(' ', '')
        x = x.split(',')
        ciphers.append((int(x[0]),int(x[1])))
    #print(ciphers)
    Prime = 211287523889848166456771978073530465593093161450010064509303400255860514422619
    Generator = 15944282073914562075116370489962003433567850159612874030242082495627173757989
    Exponent = 102112374625719848836417645466897582644268266380360636462856219195606277562091
    b = 102112374625719848836417645466897582644268266380360636462856219195606277562091

    res = ''
    for x in ciphers:
        half_mask = x[0]
        cipher = x[1]
        full_mask = pow(half_mask, b, Prime)
        neg_full_mask = egcd(Prime, full_mask)[1]
        message = (cipher * neg_full_mask) % Prime
        res = res + chr(message)
    print(res)
    meh = open('Assignment4_5.txt', 'w')
    meh.write(res)
    
def main():
    #our secret half

    N = 182755680224874988969105090392374859247
    #the slope value
    a = 286458106491124997002528249079664631375
    #the prime q
    q = 231980187997634794246138521723892165531

    #our curve
    ec = (a, 0, q)

    file = open('a4.cipher', 'r')
    c = []
    
    result = []
    result2 = ''
    for x in file:
        #print(x)
        #print(x)
        x = x.replace('\n', '')
        x= x.split(' ')
        for y in x:
            c.append(int(y))
        #print(c)
        cipher_point = (c[0], c[1])
        half_mask = (c[2],c[3])
        #print(half_mask)
        #print(cipher_point)
        full_mask = multiply_point(n=N, p=half_mask, ec=ec)
        #print('full mask done')
        neg_full_mask = (full_mask[0], q - full_mask[1])
        #print(neg_full_mask)
        message = point_addition(a=cipher_point, b=neg_full_mask, ec=ec)

        test = point_addition(a=message, b=full_mask, ec=ec)

        if cipher_point != test:
            print(message)
            print(test)
            
            break
        #print(cipher_point)
        #print(message)
        #result.append('{0:1b}'.format(message[0]))
        c = []
        result.append(message)
        result2 = result2+chr(message[0])

    print(result2) 
    file = open('elgamal.keys','w')
    file.write(result2)
    #input('  asdf ')

    

if __name__ == '__main__':
    main()
    secondmain()