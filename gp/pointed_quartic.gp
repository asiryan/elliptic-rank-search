\\ Run from the project root: gp -fq gp/pointed_quartic.gp
\\ An exact example of projection from P, using no point/rank database.
E = ellinit([0,0,0,-25,4]);
P = [0,2]; Q = [5,2];
x0 = P[1]; v0 = 2*P[2]+E.a1*x0+E.a3;
D = x^4-2*(12*x0+E.b2)*x^2+32*v0*x+E.b2^2-8*E.b2*x0-48*x0^2-32*E.b4;
t = (2*Q[2]+E.a1*Q[1]+E.a3-v0)/(Q[1]-x0);
z = 8*Q[1]-t^2+E.b2+4*x0;
if(z^2 != subst(D,x,t), error("Projection identity failed"));
recover(t,z) = {my(xx=(t^2-E.b2-4*x0+z)/8); [xx,(v0+t*(xx-x0)-E.a1*xx-E.a3)/2]};
if(recover(t,z) != Q, error("Inverse identity failed"));
R = recover(t,-z);
if(!ellisoncurve(E,R), error("Companion point is off curve"));
if(elladd(E,P,elladd(E,Q,R)) != [0], error("Group identity failed"));
print("Quartic: z^2 = ", D);
print("Recovered Q: ", Q, "; companion R: ", R);
print("PROJECTION_CHECK_OK");
quit;
