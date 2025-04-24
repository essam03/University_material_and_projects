 
import java.util.*; 


public class MEET {
    public static void main(String[] args) {
		int[] key1 ={0,1,0,0,1,0,0,1,0,1}; //
		int [] key2 ={0,1,1,0,1,0,1,1,1,0};
		int counter =0;
		List<String> list=new ArrayList<String>();  
 
	    int[][] plaintexts = {
	        {1, 1, 1, 1, 0, 0, 0, 1},
	        {0, 0, 1, 1, 0, 0, 0, 1},
	        {1, 1, 1, 0, 1, 1, 0, 1},
	        {0, 0, 1, 0, 1, 0, 1, 1},
	    };
 
	    int[][] ciphertexts = {
	        {1, 0, 1, 0, 1, 0, 1, 1},
	        {0, 0, 0, 1, 1, 1, 1, 1},
	        {0, 1, 1, 0, 0, 0, 1, 1},
	        {1, 1, 0, 1, 0, 1, 1, 1},
	    };
	    // key1 = 
        // sdes_decrypt(key1, plaintexts[0]);
        
        // sdes_encrypt(key2, ciphertexts[4]);
        


        List<Map.Entry<Integer, int[]>> am1 = new ArrayList<>();
        List<Map.Entry<Integer, int[]>> am2 = new ArrayList<>();
        
        for(int i = 0;i<1024;i++){
            key1=decToBinary(i);
            int[] mid1 = sdes_encrypt(decToBinary(i), plaintexts[0]);
            am1.add(new AbstractMap.SimpleEntry<>(i, mid1));
        }

        for(int i = 0;i<1024;i++){
            key2=decToBinary(i);
            int[] mid2 = sdes_decrypt(decToBinary(i), ciphertexts[0]);
            am2.add(new AbstractMap.SimpleEntry<>(i, mid2));
        }
        List<int[]> Commonkeys = new ArrayList<>();
        int keyy1, keyy2, m1, m2;
        for(int i = 0;i<am1.size();i++){
            for(int j = 0;j<am2.size();j++){
                m1 = binaryArrayToDecimal(am1.get(i).getValue());
                m2 = binaryArrayToDecimal(am2.get(j).getValue());
                
                if(m1 == m2){
                    int pp1 = binaryArrayToDecimal(sdes_encrypt(decToBinary(am2.get(j).getKey()), sdes_encrypt(decToBinary(am1.get(i).getKey()), plaintexts[0])));
                    int cc1 = binaryArrayToDecimal(sdes_decrypt(decToBinary(am2.get(j).getKey()), sdes_decrypt(decToBinary(am1.get(i).getKey()), ciphertexts[0])));
                    
                    int pp2 = binaryArrayToDecimal(sdes_encrypt(decToBinary(am2.get(j).getKey()), sdes_encrypt(decToBinary(am1.get(i).getKey()), plaintexts[1])));
                    int cc2 = binaryArrayToDecimal(sdes_decrypt(decToBinary(am2.get(j).getKey()), sdes_decrypt(decToBinary(am1.get(i).getKey()), ciphertexts[1])));
                    
                    int pp3 = binaryArrayToDecimal(sdes_encrypt(decToBinary(am2.get(j).getKey()), sdes_encrypt(decToBinary(am1.get(i).getKey()), plaintexts[2])));
                    int cc3 = binaryArrayToDecimal(sdes_decrypt(decToBinary(am2.get(j).getKey()), sdes_decrypt(decToBinary(am1.get(i).getKey()), ciphertexts[2])));
                    
                    int pp4 = binaryArrayToDecimal(sdes_encrypt(decToBinary(am2.get(j).getKey()), sdes_encrypt(decToBinary(am1.get(i).getKey()), plaintexts[3])));
                    int cc4 = binaryArrayToDecimal(sdes_decrypt(decToBinary(am2.get(j).getKey()), sdes_decrypt(decToBinary(am1.get(i).getKey()), ciphertexts[3])));
                    

                    // System.out.println(sdes_encrypt(decToBinary(am2.get(j).getKey()), sdes_encrypt(decToBinary(am1.get(i).getKey()), plaintexts[0])));
                    if(pp1 == binaryArrayToDecimal(ciphertexts[0])
                     && pp2 == binaryArrayToDecimal(ciphertexts[1])
                     && pp3 == binaryArrayToDecimal(ciphertexts[2])
                     && pp4 == binaryArrayToDecimal(ciphertexts[3])
                     ){
                        System.out.println("Common keys " + am1.get(i).getKey() + " " + am2.get(j).getKey());
                    }
                }


            }
        }

	    // for(int i=0; i<1024;i++) {
	    // 	for(int j=0; j<1024;j++) {
	    		
	    // 		for(int l=0; l<4;l++) {
	    // 		key1=decToBinary(i);
	    // 		key2=decToBinary(j);
	    //         int[] mid1 = encrypt(key1, key2, plaintexts[l]);
	    //         int[] mid2 = decrypt(key2, key1, ciphertexts[l]);
	    //         if (Arrays.equals(key1, new int[]{0, 0, 0, 1, 1, 1, 0, 0, 1, 0}) && Arrays.equals(key2, new int[]{1, 0, 0, 0, 1, 1, 0, 0, 0, 0})) {
		//                 System.out.println(Arrays.toString(mid1));
		//                 System.out.println(Arrays.toString(mid2));  
 
	    //         }
 
	    //         if(Arrays.equals(mid1, mid2)) {
	    //         	counter++;
	    //         	list.add(Arrays.toString(key1) + ""+ Arrays.toString(key2));
	            	
	    //         	if (l==3 && counter!=3) {
	    //         		counter=0;
	    //         	}
	    //         }
	            
	    // 		}
	    	
	    // 	}
	    // }
	    
	    if(counter ==4) {
	    	for(String keyPair:list)
	        System.out.println("Common matching keys found: " + keyPair);
	    }
	    
 
	}

    public static int binaryArrayToDecimal(int[] binaryArray) {
        int decimal = 0;
        for (int i = 0; i < 8; i++) {
            decimal += binaryArray[i] * (1 << (7 - i));
        }
        return decimal;
    }

	static int[] decToBinary(int n) {
	    // Create an array to store the binary number with exactly 10 bits
	    int[] binaryNum = new int[10];
	    
	    // Initialize the array with zeros
	    for (int i = 0; i < 10; i++) {
	        binaryNum[i] = 0;
	    }
	    
	    int index = 9; // Start from the last index (rightmost bit)
 
	    // Convert decimal to binary
	    while (n > 0 && index >= 0) {
	        binaryNum[index] = n % 2;
	        n = n / 2;
	        index--;
	    }
 
	    return binaryNum;
	}
 
	static int[] encrypt(int[] k1, int[] k2, int[] plaintext) {
        // Initial Permutation
        int[] initialPerm = initialPermutation(plaintext);
 
        // Split
        int[] left = Arrays.copyOfRange(initialPerm, 0, 4);
        int[] right = Arrays.copyOfRange(initialPerm, 4, 8);
 
        // First round with k1
        int[] round1Output = fk(left, right, k1);
 
        // Swap halves
        int[] swapped = swapHalves(round1Output);
 
        // Split again
        left = Arrays.copyOfRange(swapped, 0, 4);
        right = Arrays.copyOfRange(swapped, 4, 8);
 
        // Second round with k2
        int[] round2Output = fk(left, right, k2);
 
        // Final Permutation
        int[] ciphertext = finalPermutation(round2Output);
        return ciphertext;
    }
 
    static int[] decrypt(int[] k2, int[] k1, int[] ciphertext) {
        // Initial Permutation
        int[] initialPerm = initialPermutation(ciphertext);
 
        // Split
        int[] left = Arrays.copyOfRange(initialPerm, 0, 4);
        int[] right = Arrays.copyOfRange(initialPerm, 4, 8);
 
        // First round with k2
        int[] round1Output = fk(left, right, k2);
 
        // Swap halves
        int[] swapped = swapHalves(round1Output);
 
        // Split again
        left = Arrays.copyOfRange(swapped, 0, 4);
        right = Arrays.copyOfRange(swapped, 4, 8);
 
        // Second round with k1
        int[] round2Output = fk(left, right, k1);
 
        // Final Permutation
        int[] decryptedText = finalPermutation(round2Output);
        return decryptedText;
    }
 
    // Function fk for each round
    static int[] fk(int[] left, int[] right, int[] key) {
        // Expand and permute right half
        int[] ep = EP(right);
 
        // XOR with key
        int[] xorOutput = xor(ep, key);
 
        // Split and apply S-boxes
        int[] sboxOutput = sboxes(xorOutput);
 
        // Permutation P4
        int[] p4 = p4(sboxOutput);
 
        // XOR with left half
        int[] newLeft = xor(left, p4);
 
        // Combine halves
        int[] combined = combine(newLeft, right);
        return combined;
    }
 
    static int[] xor(int[] a, int[] b) {
        int[] result = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            result[i] = a[i] ^ b[i];
        }
        return result;
    }
 
    static int[] combine(int[] left, int[] right) {
        int[] combined = new int[left.length + right.length];
        System.arraycopy(left, 0, combined, 0, left.length);
        System.arraycopy(right, 0, combined, left.length, right.length);
        return combined;
    }
 
    static int[] swapHalves(int[] input) {
        int halfLength = input.length / 2;
        int[] swapped = new int[input.length];
        System.arraycopy(input, halfLength, swapped, 0, halfLength);
        System.arraycopy(input, 0, swapped, halfLength, halfLength);
        return swapped;
    }
 
    static int[] initialPermutation(int[] input) {
        return new int[] { input[1], input[5], input[2], input[0], input[3], input[7], input[4], input[6] };
    }
 
    static int[] finalPermutation(int[] input) {
        return new int[] { input[3], input[0], input[2], input[4], input[6], input[1], input[7], input[5] };
    }
 
    static int[] p10(int[] key) {
        return new int[] { key[2], key[4], key[1], key[6], key[3], key[9], key[0], key[8], key[7], key[5] };
    }
 
    static int[] p8(int[] key) {
        return new int[] { key[5], key[2], key[6], key[3], key[7], key[4], key[9], key[8] };
    }
 
    static int[] p4(int[] input) {
        return new int[] { input[1], input[3], input[2], input[0] };
    }
 
    static int[] EP(int[] right) {
        return new int[] { right[3], right[0], right[1], right[2], right[1], right[2], right[3], right[0] };
    }
 
    static int[] shiftLeft(int[] bits, int numShifts) {
        int[] shifted = new int[bits.length];
        System.arraycopy(bits, numShifts, shifted, 0, bits.length - numShifts);
        System.arraycopy(bits, 0, shifted, bits.length - numShifts, numShifts);
        return shifted;
    }
 
    static int[] sboxes(int[] input) {
        int[] left = Arrays.copyOfRange(input, 0, 4);
        int[] right = Arrays.copyOfRange(input, 4, 8);
 
        int[] sboxOutput = new int[4];
        s0(left, sboxOutput);
        s1(right, sboxOutput);
        return sboxOutput;
    }
 
    static void s0(int[] input, int[] output) {
        int[][] s0 = {
                { 1, 0, 3, 2 },
                { 3, 2, 1, 0 },
                { 0, 2, 1, 3 },
                { 3, 1, 3, 2 }
        };
 
        int row = (input[0] << 1) + input[3];
        int col = (input[1] << 1) + input[2];
        int value = s0[row][col];
 
        output[0] = (value >> 1) & 1;
        output[1] = value & 1;
    }
 
    static void s1(int[] input, int[] output) {
        int[][] s1 = {
                { 0, 1, 2, 3 },
                { 2, 0, 1, 3 },
                { 3, 0, 1, 0 },
                { 2, 1, 0, 3 }
        };
 
        int row = (input[0] << 1) + input[3];
        int col = (input[1] << 1) + input[2];
        int value = s1[row][col];
 
        output[2] = (value >> 1) & 1;
        output[3] = value & 1;
    }
 
    // Calculate row index for S-box
    static int calculateRowIndex(int[] bits) {
        return (bits[0] << 1) | bits[3];
    }
 
    // Calculate column index for S-box
    static int calculateColumnIndex(int[] bits) {
        return (bits[1] << 1) | bits[2];
    }

    static int[] sdes_encrypt(int[] key, int[] plaintext){
        int[] newKey = p10(key);
        // System.out.println("Key: " + Arrays.toString(key));
        // System.out.println("New Key (P10): " + Arrays.toString(newKey));
 
        int[] splitL = Arrays.copyOfRange(newKey, 0, 5);
        int[] splitR = Arrays.copyOfRange(newKey, 5, 10);
        // System.out.println("Split Left: " + Arrays.toString(splitL));
        // System.out.println("Split Right: " + Arrays.toString(splitR));
 
        // Shifting left
        splitL = shiftLeft(splitL, 1);
        splitR = shiftLeft(splitR, 1);
        // System.out.println("After shifting left: " + Arrays.toString(splitL));
        // System.out.println("After shifting right: " + Arrays.toString(splitR));
 
        // Combine and permute to get K1
        int[] combinedKey = combine(splitL, splitR);
        int[] k1 = p8(combinedKey);
        // System.out.println("Combined: " + Arrays.toString(combinedKey));
        // System.out.println("K1: " + Arrays.toString(k1));
 
        // Second shifting left
        splitL = shiftLeft(splitL, 2);
        splitR = shiftLeft(splitR, 2);
        // System.out.println("After second shifting left: " + Arrays.toString(splitL));
        // System.out.println("After second shifting right: " + Arrays.toString(splitR));
 
        // Combine and permute to get K2
        combinedKey = combine(splitL, splitR);
        int[] k2 = p8(combinedKey);
        // System.out.println("Combined: " + Arrays.toString(combinedKey));
        // System.out.println("K2: " + Arrays.toString(k2));
 
        // Encryption
        int[] ciphertext = encrypt(k1, k2, plaintext);
        // System.out.println("Ciphertext: " + Arrays.toString(ciphertext));

        return ciphertext;
    }


    static int[] sdes_decrypt(int[] key, int[] plaintext){
        int[] newKey = p10(key);
        // System.out.println("Key: " + Arrays.toString(key));
        // System.out.println("New Key (P10): " + Arrays.toString(newKey));
 
        int[] splitL = Arrays.copyOfRange(newKey, 0, 5);
        int[] splitR = Arrays.copyOfRange(newKey, 5, 10);
        // System.out.println("Split Left: " + Arrays.toString(splitL));
        // System.out.println("Split Right: " + Arrays.toString(splitR));
 
        // Shifting left
        splitL = shiftLeft(splitL, 1);
        splitR = shiftLeft(splitR, 1);
        // System.out.println("After shifting left: " + Arrays.toString(splitL));
        // System.out.println("After shifting right: " + Arrays.toString(splitR));
 
        // Combine and permute to get K1
        int[] combinedKey = combine(splitL, splitR);
        int[] k1 = p8(combinedKey);
        // System.out.println("Combined: " + Arrays.toString(combinedKey));
        // System.out.println("K1: " + Arrays.toString(k1));
 
        // Second shifting left
        splitL = shiftLeft(splitL, 2);
        splitR = shiftLeft(splitR, 2);
        // System.out.println("After second shifting left: " + Arrays.toString(splitL));
        // System.out.println("After second shifting right: " + Arrays.toString(splitR));
 
        // Combine and permute to get K2
        combinedKey = combine(splitL, splitR);
        int[] k2 = p8(combinedKey);
        // System.out.println("Combined: " + Arrays.toString(combinedKey));
        // System.out.println("K2: " + Arrays.toString(k2));
 
        // Encryption
        int[] decryptedText = decrypt(k2, k1, plaintext);
        // System.out.println("Decrypted Text: " + Arrays.toString(decryptedText));
    
        return decryptedText;
    }
}