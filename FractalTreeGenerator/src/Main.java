/**
 * Simple main used for calling the proper classes
 *
 * @author  beedle-cmyk
 * @version 12/6/2024
 */
public class Main {

    /**
     * Constructor used to get clean Xdoclint
     */
    public Main(){
        //does nothing
    }

    /**
     * loading main
     * @param args string args parameters
     */
    public static void main(String[] args) {
        FractalSubject subject = new FractalGenerator();
        new FractalGui(subject);
        new FractalDrawing(subject);
    }
}