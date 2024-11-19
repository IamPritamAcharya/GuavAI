import java.util.*;

public class test2 {
public static int[] getConcatenation(int[] nums) {
    int n = nums.length;
    int[] ans = new int[2 * n];
    for (int i = 0; i < n; ++i) {
      ans[i] = nums[i];
      ans[i + n] = nums[i];
    }
    return ans;
  }
public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
int[] a = {1,2,3};
int[] ans = getConcatenation(a);
for(int i = 0; i<ans.length ;i++) {
System.out.println(ans[i] + ", ");
}
}
}
