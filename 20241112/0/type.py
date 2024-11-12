class A: pass
class B: pass

class C(A, B): pass
class D(B, A): pass

#class E(A, C): pass
class E(C, A): pass

#class E(B, C): pass
class E(C, B): pass

#class E(C, D): pass
#class E(D, C): pass
class D(A, B): pass
class E(C, D): pass
