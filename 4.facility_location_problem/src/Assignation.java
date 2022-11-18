import java.util.ArrayList;
import java.util.HashMap;

public class Assignation {

    HashMap<DistributionCenter, ArrayList<Customers>> assignationMap;
    ArrayList<Customers> customersAssigned;

    public  Assignation(){
        this.assignationMap = new HashMap<>();
        this.customersAssigned = new ArrayList<>();
    }

    public ArrayList<Customers> getDistributionAssignation(DistributionCenter distributionCenter){
        return this.assignationMap.get(distributionCenter);
    }

    public void addCostumerToDistributor(Customers customers, DistributionCenter distributionCenter){
        if (!assignationMap.containsKey(distributionCenter)){
            this.assignationMap.put(distributionCenter, new ArrayList<>());
        }
        this.assignationMap.get(distributionCenter).add(customers);
        this.customersAssigned.add(customers);
    }

    public DistributionCenter getDistributionCenterAssignTo(Customers customers){
        for (DistributionCenter distributionCenter: assignationMap.keySet()){
            ArrayList<Customers> customersAssignToDistributionCenter = assignationMap.get(distributionCenter);
            if (customersAssignToDistributionCenter.contains(customers)) {
                return distributionCenter;
            }
        }
        return null;
    }

    public double availableCapacity(DistributionCenter distributionCenter){
        double capacityUsed = 0.0;
        if (assignationMap.containsKey(distributionCenter)) {
            for (Customers customers : assignationMap.get(distributionCenter)) {
                capacityUsed += customers.demand;
            }
        }
        return distributionCenter.capacity - capacityUsed;
    }

    public double getCostOfAssignation(Customers customers, DistributionCenter distributionCenter){
        double totalCost = 0.0;
        if (!assignationMap.containsKey(distributionCenter)){
            totalCost += distributionCenter.setupCost;
        }
        totalCost += customers.distanceTo(distributionCenter);
        return totalCost;
    }

    public double getTotalSetupCost(){
        double totalSetupCost = 0.0;
        for (DistributionCenter distributionCenter: this.assignationMap.keySet()){
            if (this.assignationMap.get(distributionCenter).size() != 0){
                totalSetupCost += distributionCenter.setupCost;
            }
        }
        return totalSetupCost;
    }

    public double getTotalTravelCost(){
        double totalTravelCost = 0.0;
        for (DistributionCenter distributionCenter: this.assignationMap.keySet()){
            for (Customers customers: this.assignationMap.get(distributionCenter)){
                totalTravelCost += distributionCenter.distanceTo(customers);
            }
        }
        return totalTravelCost;
    }

    public double getTotalAssignationCost(){
        return getTotalSetupCost() + getTotalTravelCost();
    }

    public String getSolutionInOutputFormat(){
        StringBuilder outputResult = new StringBuilder();
        outputResult.append(this.getTotalAssignationCost());
        outputResult.append(" 0" + "\n");
        int[] outputVector = new int[this.customersAssigned.size()];
        for (Customers customers: this.customersAssigned){
            outputVector[customers.index] = getDistributionCenterAssignTo(customers).index;
        }
        outputResult.append(outputVector[0]);
        for (int i=1; i<outputVector.length; i++){
            outputResult.append(" ");
            outputResult.append(outputVector[i]);
        }
        return outputResult.toString();
    }

}
