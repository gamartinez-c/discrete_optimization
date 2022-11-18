import java.util.ArrayList;
import java.util.HashSet;

public class GreedySolver {

    public ArrayList<DistributionCenter> distributionCenters;
    public ArrayList<Customers> customers;
    public Assignation assignation;

    public GreedySolver(ArrayList<DistributionCenter> distributionCenters, ArrayList<Customers> customers){
        this.distributionCenters = distributionCenters;
        this.customers = customers;
        this.assignation = new Assignation();
    }

    public void solve(){
        ArrayList<Customers> orderOfCostumers = getCostumersOrderByDemand();
        ArrayList<DistributionCenter> orderDistributionCenters = getDistributionCentersOrderBySetupCost();

        for (Customers customer: orderOfCostumers){
            DistributionCenter selectedDistributionCenter = null;
            double selectionCost = Double.POSITIVE_INFINITY;
//            System.out.print("Customer:");
//            System.out.println(customer);
            for (DistributionCenter distributionCenter: orderDistributionCenters){
                double availableCapacity = this.assignation.availableCapacity(distributionCenter);
                double assignationCost = this.assignation.getCostOfAssignation(customer, distributionCenter);
//                System.out.print("    DistCent");
//                System.out.print(distributionCenter);
//                System.out.println(", Available Capacity: " + availableCapacity + ", AssCost: " + assignationCost);
                if (availableCapacity >= customer.demand && assignationCost < selectionCost){
                    selectedDistributionCenter = distributionCenter;
                    selectionCost = assignationCost;
                }
            }
            if(selectedDistributionCenter == null) {
                selectedDistributionCenter = getDistributionCenterWithMostAvailableCapacity();
            }
//            System.out.println("        Selected: " + selectedDistributionCenter.index);
            this.assignation.addCostumerToDistributor(customer, selectedDistributionCenter);
        }
    }

    public DistributionCenter getDistributionCenterWithMostAvailableCapacity(){
        DistributionCenter selectedDistributionCenter = distributionCenters.get(0);
        double distributionCenterAvailability = this.assignation.availableCapacity(selectedDistributionCenter);
        for (DistributionCenter distributionCenter: distributionCenters){
            if (this.assignation.availableCapacity(distributionCenter) > distributionCenterAvailability){
                selectedDistributionCenter = distributionCenter;
                distributionCenterAvailability = this.assignation.availableCapacity(selectedDistributionCenter);
            }
        }
        return selectedDistributionCenter;
    }


    public ArrayList<Customers> getCostumersOrderByDemand(){
        ArrayList<Customers> orderList = new ArrayList<>(customers);
        for (int i = 0; i < orderList.size() - 1; i++){
            for (int j = i; j < orderList.size(); j++){
                if (orderList.get(i).demand < orderList.get(j).demand){
                    Customers customerI = orderList.get(i);
                    Customers customerJ = orderList.get(j);
                    orderList.remove(customerI);
                    orderList.remove(customerJ);
                    orderList.add(i, customerJ);
                    orderList.add(j, customerI);
                }
            }
        }
        return orderList;
    }

    public ArrayList<DistributionCenter> getDistributionCentersOrderBySetupCost(){
        ArrayList<DistributionCenter> orderList = new ArrayList<>(this.distributionCenters);
        for (int i = 0; i < orderList.size() - 1; i++){
            for (int j = i; j < orderList.size(); j++){
                if (orderList.get(i).setupCost > orderList.get(j).setupCost){
                    DistributionCenter distributionCenterI = orderList.get(i);
                    DistributionCenter distributionCenterJ = orderList.get(j);
                    orderList.remove(distributionCenterI);
                    orderList.remove(distributionCenterJ);
                    orderList.add(i, distributionCenterJ);
                    orderList.add(j, distributionCenterI);
                }
            }
        }
        return orderList;
    }
}
