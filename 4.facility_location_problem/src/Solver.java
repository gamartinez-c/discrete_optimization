import java.io.*;
import java.util.List;
import java.util.ArrayList;

public class Solver {
    public static void main(String[] args) {
        try {
            solve(args);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static void solve(String[] args) throws IOException {
        String fileName = null;
        
        // get the temp file name
        for(String arg : args){
            if(arg.startsWith("-file=")){
                fileName = arg.substring(6);
            } 
        }
        if(fileName == null)
            return;
        
        // read the lines out of the file
        List<String> lines = new ArrayList<String>();
        BufferedReader input =  new BufferedReader(new FileReader(fileName));
        try {
            String line = null;
            while (( line = input.readLine()) != null){
                lines.add(line);
            }
        }
        finally {
            input.close();
        }

        // parse the data in the file
        String[] firstLine = lines.get(0).split("\\s+");
        int numberOfFacilities = Integer.parseInt(firstLine[0]);
        int numberOfCustomers = Integer.parseInt(firstLine[1]);

        ArrayList<DistributionCenter> distributionCenters = new ArrayList<DistributionCenter>();
        for (int i = 0; i < numberOfFacilities; i++){
            int indexInInput = i + 1;
            String distributionCenterData = lines.get(indexInInput);
            String[] parts = distributionCenterData.split("\\s+");

            double setupCost = Double.parseDouble(parts[0]);
            double capacity = Double.parseDouble(parts[1]);
            double x = Double.parseDouble(parts[2]);
            double y = Double.parseDouble(parts[3]);
            distributionCenters.add(new DistributionCenter(x,y,capacity, setupCost, i));
        }

        ArrayList<Customers> customers = new ArrayList<Customers>();
        for (int i = 0; i < numberOfCustomers; i++){
            int indexInInput = i + numberOfFacilities + 1;
            String customerData = lines.get(indexInInput);
            String[] parts = customerData.split("\\s+");

            double demand = Double.parseDouble(parts[0]);
            double x = Double.parseDouble(parts[1]);
            double y = Double.parseDouble(parts[2]);
            customers.add(new Customers(x, y, demand, i));
        }

        GreedySolver greedySolver = new GreedySolver(distributionCenters, customers);
        greedySolver.solve();
        String outputResult = greedySolver.assignation.getSolutionInOutputFormat();

        System.out.println(outputResult);

//        prepare the solution in the specified output format
//        System.out.println(value+" 0");
//        for(int i=0; i < items; i++){
//            System.out.print(taken[i]+" ");
//        }
//        System.out.println("");
    }
}