package hk.edu.polyu.comp.comp2021.assignment2.employee;

/**
 * Levels of salary.
 */
public enum SalaryLevel {
    ENTRY(1), JUNIOR(1.25), SENIOR(1.5), EXECUTIVE(2);
    private double scale;
    // Task 1.5: Add missing code here.
    SalaryLevel(double scale) {
        this.scale = scale;
    }
    double getScale() {
        return scale;
    }
}