package hk.edu.polyu.comp.comp2021.assignment1;

public class TinyFloat {

    public static final int TINy_FLOAT_SIZE = 8;
    public static final int SIGN_POS = 0;
    public static final int ExPONENT_POS = 1;
    public static final int MANTISSA_POS = 5;


    public static void main(String[] args){
        System.out.println(numberOfIntegers());
    }

    // Task 1a: Complete the method binary2Integer
    // to convert the string value to integer value for the exponent.

    // Get number s[l, r] (non-negative)
    private static int get(String s, int l, int r) {
        int x = 0;
        for (int i = l; i <= r; i++)
            x = x * 2 + s.charAt(i) - '0';
        return x;
    }
    // Get number s[l, r] (Two-complement)
    private static int getTwoCom(String s, int l, int r) {
        return get(s, l + 1, r) - get(s, l, l) * (1 << (r - l));
    }

    private static int binary2Integer(String exponentString){
        return getTwoCom(exponentString, 0, exponentString.length() - 1);
    }

    // Task 1b: Complete the method binary2Decimal
    // to convert the string value to float value for the mantissa.
    private static float binary2Decimal(String mantissaString){
        return 1 + (float)get(mantissaString, 0, mantissaString.length() - 1) / (1 << mantissaString.length());
    }

    private static float pow2(int x) {
        return (float)(x > 0 ? (1 << x) : 1.0 / (1 << (-x)));
    }

    public static float fromString(String bitSequence){
        float result = 0;
        // Task 1c: Complete the method fromString based on the two methods,
        // binary2Integer and binary2Decimal.
        float sign = get(bitSequence, SIGN_POS, SIGN_POS) == 1 ? -1 : 1;
        int exp = binary2Integer(bitSequence.substring(ExPONENT_POS, MANTISSA_POS));
        float val = binary2Decimal(bitSequence.substring(MANTISSA_POS, TINy_FLOAT_SIZE));
        float ans = sign * val * pow2(exp);
        return ans;
    }



    public static int numberOfIntegers(){
        // Task 2: return the number of TinyFloat object values that are integers
        String[] s = getValidTinyFloatBitSequences();
        int cnt = 0;
        for (String v: s) {
            float w = fromString(v);
            int u = (int)w;
            if (u == w) {
                System.out.println(v + " == " + u);
                cnt++;
            }
        }
        return cnt;
    }

    /**
     * Get all valid bit sequences for tinyFloat values.
     * Do not change the function.
     */
    private static String[] getValidTinyFloatBitSequences(){
        int nbrValues = (int)Math.pow(2, TINy_FLOAT_SIZE);

        String[] result = new String[nbrValues];
        for(int i = 0; i < nbrValues; i++){
            result[i] = String.format("%" + TINy_FLOAT_SIZE + "s", Integer.toBinaryString(i))
                    .replace(' ', '0');
        }
        return result;
    }


}
