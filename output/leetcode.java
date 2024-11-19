import java.util.*;

public class leetcode {
public static void sortColors(int[] nums) {
boolean swapped;
for(int i = 0; i < nums.length; i++) {
swapped = false;
for(int j = 1; j < nums.length; j++) {
if(nums[j]<nums[j-1]) {
int k = nums[j];
nums[j] = nums[j-1];
nums[j-1] = k;
swapped = true;
}
}
if (!swapped) break;
}
for(int i : nums) {
System.out.println(i);
}
}
public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
int[] arr1 = {2,0,2,1,1,0};
sortColors(arr1);
}
}
