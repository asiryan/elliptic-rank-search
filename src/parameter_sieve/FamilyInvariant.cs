using System.Numerics;

// Exact j-invariant for deduplication, independent of any elliptic-curve library.
static class FamilyInvariant
{
    public static string J(BigInteger u, BigInteger v)
    {
        var u2=u*u; var uv=u*v; var v2=v*v;
        var u4=u2*u2; var u3v=u2*uv; var u2v2=u2*v2; var uv3=uv*v2; var v4=v2*v2;
        var l=446667*u2+471466*uv+239031*v2;
        var p=318552*u2+368554*uv-72570*v2;
        var q=733413*u2-45082*uv-14960*v2;
        var d=5*(7174492962L*u4-7114589515L*u3v-22069002960L*u2v2+3909144679L*uv3-205134150*v4);
        var e=882769396002L*u4+811447034567L*u3v-1174040743L*u2v2-32493137198L*uv3-2386325360L*v4;
        var b=p*q*(l+p+q)-p*e-q*d;
        var b2=l*l+4*(d+e); var b4=l*b+2*d*e; var b6=b*b;
        var c4=b2*b2-24*b4; var c6=-b2*b2*b2+36*b2*b4-216*b6;
        var numerator=c4*c4*c4; var denominator=(numerator-c6*c6)/1728;
        if (denominator.IsZero) throw new ArgumentException("Singular family parameter");
        if (denominator.Sign<0) { numerator=-numerator; denominator=-denominator; }
        var gcd=BigInteger.GreatestCommonDivisor(numerator,denominator);
        numerator/=gcd; denominator/=gcd;
        return denominator.IsOne ? numerator.ToString() : $"{numerator}/{denominator}";
    }
}
