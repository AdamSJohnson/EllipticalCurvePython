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

def point_addition(a=(-1,-1), b=(-1,-1), field=[], ec = (-1,-1,-1)):
	#call must pass new values
	if a == (-1,-1) or b == (-1,1) or field == [] or ec[2] == -1:
		print('change em')
		return 0
	q = ec[2]
	#make sure we are adding points in the field
	if a in field and b in field:
		print('good')
		#case 1 a.x != b.x
		if a[0] != b[0]:
			#different point addition
			#get y and do correct negative modulus
			y_comp = a[1] - b[1]
			while y_comp < 0:
				y_comp += q
			#get x and do correct negative modulus
			x_comp = a[0]-b[0]
			while x_comp < 0:
				x_comp += q
			y_comp = y_comp % q
			x_comp = x_comp % q

			#calculate m 
			m =  y_comp * egcd(q, x_comp)[1] 
			m = m % q
			#solve the lines
			x_r = pow(m, 2) - (a[0] + b[0])
			while x_r < 0:
				x_r += q
			x_r = x_r % q
			y_r = a[1] + m * (x_r - a[0])
			while y_r < 0:
				y_r += q
			y_r = y_r % q

			if (x_r, y_r) in field:
				return (x_r, q - y_r)
			else:
				return 0
		#point doubling case
		if a == b:
			#calculat the x part of m
			m_x = 3*pow(a[0], 2) + ec[0]
			#do correct negative modulus
			while m_x < 0:
				m_x += q
			#correct positive mod
			m_x = m_x % q

			#calculate the y inverse
			m_y = 2 * a[1]
			while m_y < 0:
				m_y += q
			m_y = m_y % q
			m_y = egcd(q, m_y)[1]

			#get the full m
			m = m_x * m_y
			m = m % q

			x_r = pow(m, 2) - 2 * a[0]
			while x_r < 0:
				x_r += q
			x_r = x_r % q

			y_r = a[1] + m * (x_r - a[0])
			while y_r < 0:
				y_r += q
			y_r = y_r % q
			return (x_r, q - y_r)
	# if we end up here we are in the negative case p + (-p) = infinity point
	return 0

def multiply_point(n=-1, p=(-1,-1), field=[], ec=(-1,-1,-1)):
	if n < 1:
		return 0
	if p == (-1,-1) or field == [] or ec[2] == -1:
		return 0
	summed_point = (-1,-1)
	while n > 0:
		if n % 2 == 0:
			n = n/2
			p = point_addition(a=p, b=p, field=field, ec = ec)
		else:
			n = n - 1
			if summed_point == (-1,-1):
				summed_point = p
			else:
				summed_point = point_addition(a=p, b=summed_point, field=field, ec = ec)
	return summed_point

def main():
	ec = build_ec(n_bits=15)
	while ec[0] < 0:
		ec = build_ec(n_bits=15)
	#print('x^3 +' , ec[0], '* x^2 +', ec[1], 'mod', ec[2])

	ec = (0, -2, 7)
	field = generate_field(ec=ec)
	print(field)
	size = 0
	for i in field:
		size+=1
	print(size)
	z = point_addition(a=(3,2),b=(3,2), field=field, ec=ec)
	print(z)
	z = point_addition(a=(5,2),b=(6,2), field=field, ec=ec)
	print(z)
	z = point_addition(a=(3,2),b=(6,2), field=field, ec=ec)
	print(z)
	z = multiply_point(n = 5,p=(3,2), field=field, ec=ec)
	print(z)
if __name__ == '__main__':
	main()