Right now this is just the functions we leared in class. Hopefully they can help with the next assignment 
otherwise this is just a generalized ellipical curve modulo q function dump.

Functions and how they work:
gcd(a, b) gives back the gcd of a and b
egcd(a, b) gives back the modular inverse of a, and b along with the gcd (a^-1, b^-1, gcd)
isprime(n) checks if a number is prime
prime_maker(n_bits) returns with high probablity a prime that is n_bits long
build_ec(a=1, b=1, n_bits=4) given an a and b value setups an EC tuple (a, b, q)
generate_field(ec = (1,1,11)) given an ec tuple generates the field of points that solves said ec
point_addition(a=(-1,-1), b=(-1,-1), field=[], ec = (-1,-1,-1)) given points a and b and an ec gives back the a + b
    three cases: 
      1: a_x != b_x returns point tuple (x,y)
      2: a==b returns point tuple (x,y)
      3: a==-b returns 0 for infinity point
multiply_point(n=-1, p=(-1,-1), field=[], ec=(-1,-1,-1)) given an n value, a point p, a field,, and an ec generates the value
  n*p using the doubling multiplication method
