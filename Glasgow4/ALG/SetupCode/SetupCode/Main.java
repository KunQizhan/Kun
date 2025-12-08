import java.util.*;
import SuffixTreePackage.*;

/**
 * Main class - for accessing suffix tree applications
 * @author David Manlove
 */

public class Main {

	/**
	 * The main method.
	 * @param args the arguments
	 */
	public static void main(String args[]) {
		String errorMessage = "Required syntax:\n";
		errorMessage += "  java Main SearchOne <filename> <query string> for Task 1\n";
		errorMessage += "  java Main SearchAll <filename> <query string> for Task 2\n";
		errorMessage += "  java Main LRS <filename> for Task 3\n" ;
		errorMessage += "  java Main LCS <filename1> <filename2> for Task 4";

		if (args.length < 2)
			System.out.println(errorMessage);
		else {
			// Get the command from the first argument
			String command = args[0];

			switch (command) {
			case "SearchOne": {
				if (args.length < 3) {
					System.out.println(errorMessage);
					break;
				}
				
				// Read filename and query string from arguments
				String fileName = args[1];
				String queryString = args[2];
				
				// Read file content into byte array
				FileInput fileInput = new FileInput(fileName);
				byte[] text = fileInput.readFile();
				
				// Build suffix tree for the text
				SuffixTree tree = new SuffixTree(text);
				
				// Create application object and perform search
				SuffixTreeAppl appl = new SuffixTreeAppl(tree);
				Task1Info result = appl.searchSuffixTree(queryString.getBytes());
				
				// Display results
				if (result.getPos() == -1) {
					System.out.println("Search string \"" + queryString + 
					                   "\" not found in " + fileName);
				} else {
					System.out.println("Search string \"" + queryString + 
					                   "\" occurs at position " + result.getPos() + 
					                   " of " + fileName);
				}
				break;
			}
			
			case "SearchAll": {
				if (args.length < 3) {
					System.out.println(errorMessage);
					break;
				}
				
				// Read filename and query string from arguments
				String fileName = args[1];
				String queryString = args[2];
				
				// Read file content into byte array
				FileInput fileInput = new FileInput(fileName);
				byte[] text = fileInput.readFile();
				
				// Build suffix tree for the text
				SuffixTree tree = new SuffixTree(text);
				
				// Create application object and find all occurrences
				SuffixTreeAppl appl = new SuffixTreeAppl(tree);
				Task2Info result = appl.allOccurrences(queryString.getBytes());
				
				// Display results
				LinkedList<Integer> positions = result.getPositions();
				if (positions.isEmpty()) {
					System.out.println("The string \"" + queryString + 
					                   "\" does not occur in " + fileName);
				} else {
					System.out.println("The string \"" + queryString + 
					                   "\" occurs in " + fileName + " at positions:");
					for (Integer pos : positions) {
						System.out.println(pos);
					}
					System.out.println("The total number of occurrences is " + 
					                   positions.size());
				}
				break;
			}
			
			case "LRS": {
				// Read filename from arguments
				String fileName = args[1];
				
				// Read file content into byte array
				FileInput fileInput = new FileInput(fileName);
				byte[] text = fileInput.readFile();
				
				// Build suffix tree for the text
				SuffixTree tree = new SuffixTree(text);
				
				// Create application object and find LRS
				SuffixTreeAppl appl = new SuffixTreeAppl(tree);
				Task3Info result = appl.traverseForLrs();
				
				// Display results
				if (result.getLen() == 0) {
					System.out.println("No repeated substring found in " + fileName);
				} else {
					// Extract the LRS from the original text
					byte[] s = tree.getString();
					int len = result.getLen();
					int pos1 = result.getPos1();
					int pos2 = result.getPos2();
					
					byte[] lrsBytes = new byte[len];
					System.arraycopy(s, pos1, lrsBytes, 0, len);
					String lrsString = new String(lrsBytes);
					
					System.out.println("An LRS in " + fileName + " is \"" + 
					                   lrsString + "\"");
					System.out.println("Its length is " + len);
					System.out.println("Starting position of one occurrence is " + pos1);
					System.out.println("Starting position of another occurrence is " + pos2);
				}
				break;
			}
			
			case "LCS": {
				if (args.length < 3) {
					System.out.println(errorMessage);
					break;
				}
				
				// Read two filenames from arguments
				String fileName1 = args[1];
				String fileName2 = args[2];
				
				// Read both file contents into byte arrays
				FileInput fileInput1 = new FileInput(fileName1);
				byte[] text1 = fileInput1.readFile();
				
				FileInput fileInput2 = new FileInput(fileName2);
				byte[] text2 = fileInput2.readFile();
				
				// Build generalized suffix tree for both texts
				SuffixTree tree = new SuffixTree(text1, text2);
				
				// Create application object and find LCS
				SuffixTreeAppl appl = new SuffixTreeAppl(tree);
				Task4Info result = appl.traverseForLcs(text1.length);
				
				// Display results
				if (result.getLen() == 0) {
					System.out.println("No common substring found between " + 
					                   fileName1 + " and " + fileName2);
				} else {
					// Extract the LCS (from text1)
					int len = result.getLen();
					int pos1 = result.getPos1();
					int pos2 = result.getPos2();
					
					byte[] lcsBytes = new byte[len];
					System.arraycopy(text1, pos1, lcsBytes, 0, len);
					String lcsString = new String(lcsBytes);
					
					System.out.println("An LCS of " + fileName1 + " and " + 
					                   fileName2 + " is \"" + lcsString + "\"");
					System.out.println("Its length is " + len);
					System.out.println("Starting position in " + fileName1 + 
					                   " is " + pos1);
					System.out.println("Starting position in " + fileName2 + 
					                   " is " + pos2);
				}
				break;
			}
			
			default: System.out.println(errorMessage);
			}
		}
	}
}