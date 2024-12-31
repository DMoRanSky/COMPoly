package hk.edu.polyu.comp.comp2021.assignment1.complex;

import org.junit.Test;
import org.junit.Before;

import static org.junit.Assert.*;

public class ComplexTest {
    @Test
    public void testConstructor() {
        Rational real = new Rational(1, 2);
        Rational imag = new Rational(1, 3);

        Complex c1 = new Complex(real, imag);
        c1.simplify();

        assertEquals("(1/2,1/3)", c1.toString());
    }

    @Test
    public void testAddition() {
        Complex c1 = new Complex(new Rational(1, 2), new Rational(1, 3));
        Complex c2 = new Complex(new Rational(2, 3), new Rational(1, 4));

        Complex cSum = c1.add(c2);
        cSum.simplify();

        assertEquals("(7/6,7/12)", cSum.toString());
    }

    @Test
    public void testSubstraction() {
        Complex c1 = new Complex(new Rational(1, 2), new Rational(2, 3));
        Complex c2 = new Complex(new Rational(1, 3), new Rational(1, 4));

        Complex cSum = c1.subtract(c2);
        cSum.simplify();

        assertEquals("(1/6,5/12)", cSum.toString());
    }

    @Test
    public void testMultiplication() {
        Complex c1 = new Complex(new Rational(1, 4), new Rational(3, 7));
        Complex c2 = new Complex(new Rational(1, 5), new Rational(5, 8));

        Complex cMul = c1.multiply(c2);
        cMul.simplify();

        assertEquals("(-61/280,271/1120)", cMul.toString());
    }

    @Test
    public void testDivision(){
        Complex c1 = new Complex(new Rational(2, 5), new Rational(3, 7));
        Complex c2 = new Complex(new Rational(1, 3), new Rational(1, 6));
        // 1/3 + 1/6i //
        Complex cDiv = c1.divide(c2);
        cDiv.simplify();

        assertEquals("(258/175,96/175)", cDiv.toString());
    }

    @Test
    public void testDivision2(){
        Complex c1 = new Complex(new Rational(7, -8), new Rational(-2, 7));
        Complex c2 = new Complex(new Rational(9, -1), new Rational(-8, 9));
        // 1/3 + 1/6i //
        Complex cDiv = c1.divide(c2);
        System.out.println( cDiv.toString());
        cDiv.simplify();
        System.out.println( cDiv.toString());
        //assertEquals("(105/584,3/146)", cDiv.toString());
    }

    @Test
    public void testDivision3(){
        Complex c1 = new Complex(new Rational(2, 9), new Rational(5, 9));
        Complex c2 = new Complex(new Rational(7, 8), new Rational(8, 5));

        Complex cDiv = c1.divide(c2);
        cDiv.simplify();

        assertEquals("(5200/15963,1880/47889)", cDiv.toString());
    }

}
