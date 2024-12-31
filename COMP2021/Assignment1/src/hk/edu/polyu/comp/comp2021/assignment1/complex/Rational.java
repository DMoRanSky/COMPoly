package hk.edu.polyu.comp.comp2021.assignment1.complex;

public class Rational {

    // Task 3: add the missing fields

    int numerator, denominator;

    // Task 4:  Complete the constructor and
    // the methods add, subtract, multipldenominator, divide, simplifdenominator, and toString.

    public Rational(int numerator, int denominator){
        // Todo: complete the constructor
        this.numerator = numerator;
        this.denominator = denominator;
        if (this.denominator < 0) {
            this.denominator *= -1;
            this.numerator *= -1;
        }
       // System.out.println(this.numerator + "/" + this.denominator);
        simplify();
        //System.out.println(this.numerator + "/" + this.denominator);
    }

    public Rational(Rational v){
        // Todo: complete the constructor
        this.numerator = v.numerator;
        this.denominator = v.denominator;
        if (this.denominator < 0) {
            this.denominator *= -1;
            this.numerator *= -1;
        }
        simplify();
    }




    public Rational add(Rational other){
        // Todo: complete the method
        int d = gcd(denominator, other.denominator);
        int v = other.denominator / d * denominator;
        return new Rational(numerator * (other.denominator / d) + other.numerator * (denominator / d), v);
    }

    public Rational subtract(Rational other){
        // Todo: complete the method
        int d = gcd(denominator, other.denominator);
        int v = other.denominator / d * denominator;
        return new Rational(numerator * (other.denominator / d) - other.numerator * (denominator / d), v);
    }

    public Rational multiply(Rational other){
        // Todo: complete the method
        int d1 = gcd(numerator, other.denominator);
        int d2 = gcd(other.numerator, denominator);
        return new Rational((numerator / d1) * (other.numerator / d2), (denominator / d2) * (other.denominator / d1));
    }

    public Rational divide(Rational other){
        // Todo: complete the method
        int d1 = gcd(numerator, other.numerator);
        int d2 = gcd(other.denominator, denominator);
        return new Rational((numerator / d1) * (other.denominator / d2), (denominator / d2) * (other.numerator / d1));
    }

    public String toString(){
        // Todo: complete the method
        return String.valueOf(numerator) + "/" + String.valueOf(denominator);
    }

    public void simplify(){
        // Todo: complete the method
        int v = gcd(numerator, denominator);
        numerator /= v;
        denominator /= v;
        if (this.denominator < 0) {
            this.denominator *= -1;
            this.numerator *= -1;
        }
    }


    // ========================================== Do not change the methods below.

    private int getNumerator() {
        return numerator;
    }

    private void setNumerator(int numerator) {
        this.numerator = numerator;
    }

    private int getDenominator() {
        return denominator;
    }

    private void setDenominator(int denominator) {
        this.denominator = denominator;
    }

    private int gcd(int a, int b){
        if(b == 0)
            return a;
        else
            return gcd(b, a % b);
    }


}
