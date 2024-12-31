package hk.edu.polyu.comp.comp2021.assignment1.complex;

public class Complex {

    // Task 5 : add the missing fields

    Rational real, imag;

    // Task 6: Complete the constructor as well as the methods add, subtract, multiply, divide, and toString.
    public Complex(Rational real, Rational imag) {
        // Todo: complete the constructor
        this.real = real;
        this.imag = imag;
        simplify();
    }


    public Complex add(Complex other) {
        // Todo: complete the method
        return new Complex(real.add(other.real), imag.add(other.imag));
    }

    public Complex subtract(Complex other) {
        // Todo: complete the method
        return new Complex(real.subtract(other.real), imag.subtract(other.imag));
    }

    public Complex multiply(Complex other) {
        // Todo: complete the method
        Rational a = real.multiply(other.real);
        a = a.subtract(imag.multiply(other.imag));
        Rational b = real.multiply(other.imag);
        b = b.add(imag.multiply(other.real));
        return new Complex(a, b);
    }


    // 1 / this
    public Complex inv() {
        // Todo: complete the method
        // 1 / (a + bi) =  (a - bi) / a^2 + b^2
        Rational a = new Rational(real);
        Rational b = new Rational(imag);
        b.numerator = -b.numerator;
        Rational v = a.multiply(a);
        v = v.add(b.multiply(b));
        a = a.divide(v);
        b = b.divide(v);

        return new Complex(a, b);
    }

    public Complex divide(Complex other) {
        // Todo: complete the method
        // you may assume 'other' is never equal to '0+/-0i'.
        Complex v = other.inv();
        return this.multiply(v);
    }

    public void simplify() {
        // Todo: complete the method
        real.simplify();
        imag.simplify();
    }

    public String toString() {
        // Todo: complete the method
        return "(" + real.toString() + "," + imag.toString() + ")";
    }

    // =========================== Do not change the methods below


    private Rational getReal() {
        return real;
    }

    private void setReal(Rational real) {
        this.real = real;
    }

    private Rational getImag() {
        return imag;
    }

    private void setImag(Rational imag) {
        this.imag = imag;
    }
}
