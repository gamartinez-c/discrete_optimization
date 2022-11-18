import java.util.ArrayList;
import java.util.HashMap;

public class GreedySolver {

    public ArrayList<DistributionCenter> distributionCenters;
    public ArrayList<Customers> customers;
    public Assignation assignation;

    public GreedySolver(ArrayList<DistributionCenter> distributionCenters, ArrayList<Customers> customers){
        this.distributionCenters = distributionCenters;
        this.customers = customers;
        this.assignationMap = new HashMap<>();
        for (DistributionCenter distributionCenter: this.distributionCenters){
            this.assignationMap.put(distributionCenter, new ArrayList<>());
        }
    }

    public void solve(){
        ArrayList<Customers> orderOfCostumers = getCostumersOrderByDemand();
        ArrayList<DistributionCenter> orderDistributionCenters = getDistributionCentersOrderBySetupCost();

        for (Customers customer: orderOfCostumers){
            boolean customerAdded = false;
            for (DistributionCenter distributionCenter: orderDistributionCenters){
                if (this.distributionCenterCurrentCapacity(distributionCenter) >= customer.demand){
                    this.assignationMap.get(distributionCenter).add(customer);
                    customerAdded = true;
                    break;
                }
            }
            if (!customerAdded){
                DistributionCenter  distributionCenter = getDistributionCenterWithMostAvailableCapacity();
                this.assignationMap.get(distributionCenter).add(customer);
            }
        }
    }

    // FIXME:This should be in a class solution
    public double distributionCenterCurrentCapacity(DistributionCenter distributionCenter){
        double capacityUsed = 0.0;
        for (Customers customers: assignationMap.get(distributionCenter)){
            capacityUsed += customers.demand;
        }
        return capacityUsed;
    }

    public DistributionCenter getDistributionCenterWithMostAvailableCapacity(){
        DistributionCenter selectedDistributionCenter = distributionCenters.get(0);
        double distributionCenterAvailability = distributionCenterCurrentCapacity(selectedDistributionCenter);
        for (DistributionCenter distributionCenter: distributionCenters){
            if (distributionCenterCurrentCapacity(distributionCenter) > distributionCenterAvailability){
                selectedDistributionCenter = distributionCenter;
                distributionCenterAvailability = distributionCenterCurrentCapacity(selectedDistributionCenter);
            }
        }
        return selectedDistributionCenter;
    }


    public ArrayList<Customers> getCostumersOrderByDemand(){
        ArrayList<Customers> orderList = new ArrayList<>();
        while (orderList.size() != this.customers.size()){
            Customers customerToAdd = this.customers.get(0);
            for (Customers customer: this.customers){
                if (customerToAdd.demand < customer.demand ){
                    customerToAdd = customer;
                }
                orderList.add(customerToAdd);
            }
        }
        return orderList;
    }

    public ArrayList<DistributionCenter> getDistributionCentersOrderBySetupCost(){
        ArrayList<DistributionCenter> orderList = new ArrayList<>();
        while (orderList.size() != this.distributionCenters.size()){
            DistributionCenter distributionCenterToAdd = this.distributionCenters.get(0);
            for (DistributionCenter distributionCenter: this.distributionCenters){
                if (distributionCenterToAdd.setupCost < distributionCenter.setupCost ){
                    distributionCenterToAdd = distributionCenter;
                }
                orderList.add(distributionCenterToAdd);
            }
        }
        return orderList;
    }

}
