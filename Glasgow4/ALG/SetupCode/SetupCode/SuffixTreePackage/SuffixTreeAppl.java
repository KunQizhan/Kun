package SuffixTreePackage;

import java.util.*;

/**
 * Class with methods for carrying out applications of suffix trees
 * @author David Manlove
 */

public class SuffixTreeAppl {

	/** The suffix tree */
	private SuffixTree t;

	/**
	 * Default constructor.
	 */
	public SuffixTreeAppl () {
		t = null;
	}
	
	/**
	 * Constructor with parameter.
	 * 
	 * @param tree the suffix tree
	 */
	public SuffixTreeAppl (SuffixTree tree) {
		t = tree;
	}
	
	/**
	 * Search the suffix tree t representing string s for a target x.
	 * Stores -1 in Task1Info.pos if x is not a substring of s,
	 * otherwise stores p in Task1Info.pos such that x occurs in s
	 * starting at s[p] (p counts from 0)
	 * - assumes that characters of s and x occupy positions 0 onwards
	 * 
	 * @param x the target string to search for
	 * 
	 * @return a Task1Info object
	 */
	public Task1Info searchSuffixTree(byte[] x) {
		Task1Info result = new Task1Info();
		
		// Handle empty query string
		if (x == null || x.length == 0) {
			result.setPos(-1);
			return result;
		}
		
		// Get string and root node from suffix tree
		byte[] s = t.getString();
		SuffixTreeNode currentNode = t.getRoot();
		int xPos = 0;  // Current position in query string x
		
		// Start matching from root
		while (xPos < x.length) {
			// Look for child edge matching x[xPos]
			SuffixTreeNode childNode = currentNode.getChild();
			SuffixTreeNode matchedEdge = null;
			
			// Traverse sibling list to find matching edge
			while (childNode != null) {
				if (s[childNode.getLeftLabel()] == x[xPos]) {
					matchedEdge = childNode;
					break;
				}
				childNode = childNode.getSibling();
			}
			
			// No matching edge found - x is not a substring
			if (matchedEdge == null) {
				result.setPos(-1);
				return result;
			}
			
			// Continue matching along the edge
			int edgePos = matchedEdge.getLeftLabel();
			int edgeEnd = matchedEdge.getRightLabel();
			
			// Match characters on edge label
			while (edgePos <= edgeEnd && xPos < x.length) {
				if (s[edgePos] != x[xPos]) {
					// Character mismatch
					result.setPos(-1);
					return result;
				}
				edgePos++;
				xPos++;
			}
			
			// Check if we have matched all of x
			if (xPos == x.length) {
				// Find any leaf node under matched node
				int position = findLeafSuffix(matchedEdge);
				result.setPos(position);
				result.setMatchNode(matchedEdge);
				return result;
			}
			
			// Move down to continue searching
			currentNode = matchedEdge;
		}
		
		result.setPos(-1);
		return result;
	}
	
	/**
	 * Helper method to find a leaf suffix in the subtree rooted at node.
	 * 
	 * @param node the root of the subtree to search
	 * @return the suffix number of a leaf node, or -1 if not found
	 */
	private int findLeafSuffix(SuffixTreeNode node) {
		// Check if current node is a leaf
		if (node.getSuffix() != -1) {
			return node.getSuffix();
		}
		
		// Recursively search children
		SuffixTreeNode child = node.getChild();
		while (child != null) {
			int suffix = findLeafSuffix(child);
			if (suffix != -1) {
				return suffix;
			}
			child = child.getSibling();
		}
		
		return -1;
	}

	/**
	 * Search suffix tree t representing string s for all occurrences of target x.
	 * Stores in Task2Info.positions a linked list of all such occurrences.
	 * Each occurrence is specified by a starting position index in s
	 * (as in searchSuffixTree above).  The linked list is empty if there
	 * are no occurrences of x in s.
	 * - assumes that characters of s and x occupy positions 0 onwards
	 * 
	 * @param x the target string to search for
	 * 
	 * @return a Task2Info object
	 */
	public Task2Info allOccurrences(byte[] x) {
		Task2Info result = new Task2Info();
		
		// First use Task 1 to find if x exists and get the matched node
		Task1Info task1Result = searchSuffixTree(x);
		
		// If x is not found, return empty list
		if (task1Result.getPos() == -1) {
			return result;
		}
		
		// Collect all leaf suffixes from the subtree of the matched node
		SuffixTreeNode matchNode = task1Result.getMatchNode();
		collectAllLeaves(matchNode, result);
		
		return result;
	}
	
	/**
	 * Helper method to collect all leaf suffix numbers in the subtree rooted at node.
	 * Adds each suffix number to the result's position list.
	 * 
	 * @param node the root of the subtree to traverse
	 * @param result the Task2Info object to store positions in
	 */
	private void collectAllLeaves(SuffixTreeNode node, Task2Info result) {
		// If this is a leaf node, add its suffix number
		if (node.getSuffix() != -1) {
			result.addEntry(node.getSuffix());
			return;
		}
		
		// Otherwise, recursively collect from all children
		SuffixTreeNode child = node.getChild();
		while (child != null) {
			collectAllLeaves(child, result);
			child = child.getSibling();
		}
	}

	/**
	 * Traverses suffix tree t representing string s and stores ln, p1 and
	 * p2 in Task3Info.len, Task3Info.pos1 and Task3Info.pos2 respectively,
	 * so that s[p1..p1+ln-1] = s[p2..p2+ln-1], with ln maximal;
	 * i.e., finds two embeddings of a longest repeated substring of s
	 * - assumes that characters of s occupy positions 0 onwards
	 * so that p1 and p2 count from 0
	 * 
	 * @return a Task3Info object
	 */
	public Task3Info traverseForLrs () {
		Task3Info result = new Task3Info();
		
		// Start DFS from root with initial depth 0
		SuffixTreeNode root = t.getRoot();
		findLongestRepeatedSubstring(root, 0, result);
		
		return result;
	}
	
	/**
	 * Helper method to recursively find the longest repeated substring.
	 * Uses DFS to traverse the tree and tracks string depth at each node.
	 * 
	 * @param node the current node being visited
	 * @param depth the string depth from root to this node
	 * @param result the Task3Info object to store the best result
	 */
	private void findLongestRepeatedSubstring(SuffixTreeNode node, int depth, Task3Info result) {
		// Leaf nodes don't represent repeated substrings
		if (node.getSuffix() != -1) {
			return;
		}
		
		// Internal nodes (non-leaf, non-root) represent repeated substrings
		// Check if this node gives us a longer repeated substring
		if (node != t.getRoot() && depth > result.getLen()) {
			// Find two different leaf nodes in this subtree
			int[] twoLeaves = findTwoDifferentLeaves(node);
			if (twoLeaves[0] != -1 && twoLeaves[1] != -1) {
				result.setLen(depth);
				result.setPos1(twoLeaves[0]);
				result.setPos2(twoLeaves[1]);
			}
		}
		
		// Recursively process all children
		SuffixTreeNode child = node.getChild();
		while (child != null) {
			int edgeLength = child.getRightLabel() - child.getLeftLabel() + 1;
			findLongestRepeatedSubstring(child, depth + edgeLength, result);
			child = child.getSibling();
		}
	}
	
	/**
	 * Helper method to find two different leaf nodes in the subtree.
	 * Returns their suffix numbers as the two occurrence positions.
	 * 
	 * @param node the root of the subtree
	 * @return array of two suffix numbers, or [-1, -1] if not found
	 */
	private int[] findTwoDifferentLeaves(SuffixTreeNode node) {
		int[] result = new int[] {-1, -1};
		LinkedList<Integer> leaves = new LinkedList<>();
		collectLeafSuffixes(node, leaves);
		
		if (leaves.size() >= 2) {
			result[0] = leaves.get(0);
			result[1] = leaves.get(1);
		}
		
		return result;
	}
	
	/**
	 * Helper method to collect all leaf suffix numbers in a subtree.
	 * 
	 * @param node the root of the subtree
	 * @param leaves the list to store suffix numbers in
	 */
	private void collectLeafSuffixes(SuffixTreeNode node, LinkedList<Integer> leaves) {
		if (node.getSuffix() != -1) {
			leaves.add(node.getSuffix());
			return;
		}
		
		SuffixTreeNode child = node.getChild();
		while (child != null) {
			collectLeafSuffixes(child, leaves);
			child = child.getSibling();
		}
	}

	/**
	 * Traverse generalised suffix tree t representing strings s1 (of length
	 * s1Length), and s2, and store ln, p1 and p2 in Task4Info.len,
	 * Task4Info.pos1 and Task4Info.pos2 respectively, so that
	 * s1[p1..p1+ln-1] = s2[p2..p2+ln-1], with len maximal;
	 * i.e., finds embeddings in s1 and s2 of a longest common substring 
	 * of s1 and s2
	 * - assumes that characters of s1 and s2 occupy positions 0 onwards
	 * so that p1 and p2 count from 0
	 * 
	 * @param s1Length the length of s1
	 * 
	 * @return a Task4Info object
	 */
	public Task4Info traverseForLcs (int s1Length) {
		Task4Info result = new Task4Info();
		
		// First, mark all nodes with information about their leaf descendants
		SuffixTreeNode root = t.getRoot();
		markLeafDescendants(root, s1Length);
		
		// Then find the deepest node that has leaves from both strings
		findLongestCommonSubstring(root, 0, s1Length, result);
		
		return result;
	}
	
	/**
	 * Helper method to mark each node with information about leaf descendants.
	 * Uses post-order traversal to propagate information from leaves upward.
	 * 
	 * @param node the current node being processed
	 * @param s1Length the length of the first string
	 * @return Task4Info containing information about this node's descendants
	 */
	private Task4Info markLeafDescendants(SuffixTreeNode node, int s1Length) {
		// If this is a leaf node
		if (node.getSuffix() != -1) {
			int suffix = node.getSuffix();
			if (suffix < s1Length) {
				// Leaf from string 1
				node.setLeafNodeString1(true);
				node.setLeafNodeNumString1(suffix);
				return new Task4Info(0, suffix, -1, true, false);
			} else {
				// Leaf from string 2 (adjust position by subtracting s1Length + 1 for '$')
				node.setLeafNodeString2(true);
				node.setLeafNodeNumString2(suffix - s1Length - 1);
				return new Task4Info(0, -1, suffix - s1Length - 1, false, true);
			}
		}
		
		// Internal node: collect information from all children
		boolean hasString1 = false;
		boolean hasString2 = false;
		int pos1 = -1;
		int pos2 = -1;
		
		SuffixTreeNode child = node.getChild();
		while (child != null) {
			Task4Info childInfo = markLeafDescendants(child, s1Length);
			
			if (childInfo.getString1Leaf()) {
				hasString1 = true;
				if (pos1 == -1) {
					pos1 = childInfo.getPos1();
				}
			}
			
			if (childInfo.getString2Leaf()) {
				hasString2 = true;
				if (pos2 == -1) {
					pos2 = childInfo.getPos2();
				}
			}
			
			child = child.getSibling();
		}
		
		// Mark current node with collected information
		node.setLeafNodeString1(hasString1);
		node.setLeafNodeString2(hasString2);
		if (hasString1) {
			node.setLeafNodeNumString1(pos1);
		}
		if (hasString2) {
			node.setLeafNodeNumString2(pos2);
		}
		
		return new Task4Info(0, pos1, pos2, hasString1, hasString2);
	}
	
	/**
	 * Helper method to find the longest common substring.
	 * Traverses the marked tree to find the deepest node with leaves from both strings.
	 * 
	 * @param node the current node being visited
	 * @param depth the string depth from root to this node
	 * @param s1Length the length of the first string
	 * @param result the Task4Info object to store the best result
	 */
	private void findLongestCommonSubstring(SuffixTreeNode node, int depth, 
											int s1Length, Task4Info result) {
		// If this node has leaf descendants from both strings
		if (node.getLeafNodeString1() && node.getLeafNodeString2()) {
			// Check if this gives us a longer common substring
			if (depth > result.getLen()) {
				result.setLen(depth);
				result.setPos1(node.getLeafNodeNumString1());
				result.setPos2(node.getLeafNodeNumString2());
			}
		}
		
		// Recursively process all children
		SuffixTreeNode child = node.getChild();
		while (child != null) {
			int edgeLength = child.getRightLabel() - child.getLeftLabel() + 1;
			findLongestCommonSubstring(child, depth + edgeLength, s1Length, result);
			child = child.getSibling();
		}
	}
}
