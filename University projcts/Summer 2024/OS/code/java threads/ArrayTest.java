package threads;

public class ArrayTest {
	
	private int[][] Arr;
	private int[] sum;
	private int[] param;
	private int s=0;
	
	public ArrayTest() {
		Arr=new int[100][100];
		for(int i=0;i<100;i++) {
			for(int j=0;j<100;j++) {
				Arr[i][j]=i+j;
			}
		}
		sum=new int[4];
		param=new int[4];
		
		for(int i=0;i<4;i++) {
			sum[i]=0;
			param[i]=i;
		}
		
			
	}
	
	public void findTotalSum() {
		for(int i=0;i<4;i++)
			s+=sum[i];
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ArrayTest arrayTest=new ArrayTest();
		Thread[] worker=new Thread[4];
		for(int i=0;i<4;i++) {
			worker[i]=new Thread(new Sumation(arrayTest.param[i],arrayTest.Arr,arrayTest.sum));
			worker[i].start();
		}
		
		try {
			for(int i=0;i<4;i++)
				worker[i].join();
		}catch(InterruptedException ie) {
			ie.printStackTrace();
		}
		
		arrayTest.findTotalSum();
		System.out.println("sum= "+arrayTest.s);
		
	}

}
