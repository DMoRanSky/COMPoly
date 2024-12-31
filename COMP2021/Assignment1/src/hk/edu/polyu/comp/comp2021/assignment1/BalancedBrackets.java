package hk.edu.polyu.comp.comp2021.assignment1;

import java.util.Stack;

public class BalancedBrackets {

    public static boolean isBalanced(String str){
        // Task 7: Return true if and only if 'str' 1) is non-empty,
        // 2) contains only the six characters, and
        // 3) is balanced.
        int n = str.length(), top = 0;
        if (n == 0) return false;
        char[] s = new char[n + 1];
        for (int i = 0; i < n; i++) {
            char c = str.charAt(i);
            if (c == '(' || c == '[' || c == '{') {
                s[++top] = c;
            } else if (c == ')' || c == ']' || c == '}'){
                if (top == 0) return false;
                char t = s[top--];
                if (c == ')' && t != '(') return false;
                if (c == ']' && t != '[') return false;
                if (c == '}' && t != '{') return false;
            } else return false;
        }
        return top == 0;
    }
}
