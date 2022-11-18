public class DistributionCenter extends Node{
    double capacity;
    double setupCost;
    int index;

    public DistributionCenter(double x, double y, double capacity, double setupCost, int index){
        super(x, y);
        this.capacity = capacity;
        this.setupCost = setupCost;
        this.index = index;
    }
}

