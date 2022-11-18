abstract class Node {
    double x;
    double y;

    public Node(double x, double y){
        this.x = x;
        this.y = y;
    }

    public double distanceTo(Node otherNode){
        double xDistance = this.x - otherNode.x;
        double yDistance = this.y - otherNode.y;
        double squareXDistance = Math.pow(xDistance, 2);
        double squareYDistance = Math.pow(yDistance, 2);
        return Math.sqrt(squareXDistance + squareYDistance);
    }

}
