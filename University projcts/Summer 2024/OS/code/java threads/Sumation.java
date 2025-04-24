package threads;

public class Sumation implements Runnable {
	
	private int num;
	private int[][] Arr;
	private int[] sum;
	
	public Sumation(int num, int[][] arr, int[] sum) {
		this.num = num;
		Arr = arr;
		this.sum = sum;
	}



	@Override
	public void run() {
		
		System.out.println("Thread "+num+" Started");
		for(int i=num*25;i<(num+1)*25;i++) {
			for(int j=0;j<100;j++) {
				sum[num]=sum[num]+Arr[i][j];
			}
			
		}
		System.out.println("Thread "+num+" Ended");
		
	}

}
