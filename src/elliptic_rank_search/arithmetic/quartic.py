"""PARI/GP formulas for reducing quartics and composing inverse maps."""

def quartic_reduction_code(minimal=False):
    if not minimal:
        return 'C=hyperellred(F,&m);'
    return ('C0=hyperellminimalmodel(F,&m0);C=hyperellred(C0,&m1);' +
            'md=m1[2][2,1]*x+m1[2][2,2];' +
            'mh=m0[1]*m1[3]+subst(m0[3],x,(m1[2][1,1]*x+m1[2][1,2])/md)*md^2;' +
            'm=[m0[1]*m1[1],m0[2]*m1[2],mh];')
