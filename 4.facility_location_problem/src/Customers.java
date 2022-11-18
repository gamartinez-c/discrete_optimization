public class Customers extends Node{

    double demand;
    int index;

    public Customers(double x, double y, double demand, int index){
        super(x, y);
        this.demand = demand;
        this.index = index;
    }

    @Override
    public String toString() {
        return "Id: " + index + ", Demand:" + demand;
    }
}
