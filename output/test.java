import java.util.*;

public class test {
public static int sum(int[] arr) {
int sum = 0;
for(int i = 0; i < arr.length; i++) {
sum+=arr[i];
}
return sum;
}
public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
int[] arr1 = {1,2,3,3};
System.out.println(sum(arr1));
}
}
