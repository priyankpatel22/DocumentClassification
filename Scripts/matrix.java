/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Vector;

/**
 *
 * @author priyankpatel
 */
public class matrix 
{
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) throws FileNotFoundException, IOException 
    {
        BufferedReader br = new BufferedReader(new FileReader("/Users/priyankpatel/Documents/WordFreq.csv"));
        BufferedWriter bwrMatrix = new BufferedWriter(new FileWriter("/Users/priyankpatel/Documents/Matrix.csv"));
        BufferedWriter bwrWords = new BufferedWriter(new FileWriter("/Users/priyankpatel/Documents/WordList.txt"));
        BufferedWriter bwrFiles = new BufferedWriter(new FileWriter("/Users/priyankpatel/Documents/FileList.txt"));
        
        String line = "";
        Vector<String> words = new Vector<String> ();
        Vector<String> files = new Vector<String> ();
        String strArray[] = new String[3];
        String Matrix[][] = new String [101][10000];
        int posi = 0, posj = 1, posj1;
        
        for(int i = 0; i < 101;i++)
        {
            for(int j = 0; j < 10000;j++)
            {
                if(i == 0 && j == 0)
                {
                    Matrix[0][0] = "BLANK";
                }
                else
                {
                    Matrix[i][j] = "0";
                }
            }
        }
        
        while((line = br.readLine()) != null)
        {
            strArray = line.split(",");
            if(!files.contains(strArray[2]))
            {
                posi++;
                //System.out.println(posi);
                Matrix[posi][0] = strArray[2];
                files.add(strArray[2]);
                bwrFiles.write(strArray[2]);
                bwrFiles.write(",");
                posi = files.indexOf(strArray[2]) + 1;
                
            }
            if(words.contains(strArray[0]))
            {
                posj1 = words.indexOf(strArray[0]);
                Matrix[posi][posj1] = strArray[1];
            }
            else
            {
                words.add(strArray[0]);
                Matrix[0][posj] = strArray[0];
                System.out.println(Matrix[0][posj]);
                bwrWords.write(strArray[0]);
                bwrWords.write(",");
                posj = words.indexOf(strArray[0]) + 2;
                Matrix[posi][posj-1] = strArray[1];
                
            }
        }
        
        for(int i = 0; i < 101;i++)
        {
            for(int j = 0; j < 10000;j++)
            {
                //System.out.println(Matrix[i][j]);
                //System.out.println(Matrix[i][j]);
                bwrMatrix.write(Matrix[i][j]);
                bwrMatrix.write(",");
                //System.out.print(Matrix[i][j]);
                //System.out.print(",");
            }
            bwrMatrix.write("\n");
            //System.out.println("");
        }
        System.out.println(words.size());
        bwrMatrix.close();
        bwrWords.close();
        bwrFiles.close();
        
    }
}
