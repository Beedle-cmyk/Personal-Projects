import java.awt.*;
import java.util.ArrayList;

/**
 * Is responsible for generating fractal data (using recursion) and storing it in an
 * ArrayList. Each recursive call is responsible for adding one branch to the list, calculating data
 * necessary for child branches, then making a recursive call for each of the two child branches.
 *
 * @author  beedle-cmyk
 * @version 12/6/2024
 *
 */
public class FractalGenerator implements FractalSubject {

    /** List of observers that are notified on changes */
    private ArrayList<FractalObserver> observers = new ArrayList<FractalObserver>();
    /** List of fractal elements */
    private ArrayList<FractalElement> fractalElements = new ArrayList<FractalElement>();

    /** Array of slider data to adjust fractal parameters */
    private int[] sliderData;
    /** Array of color data to adjust color of fractals */
    private Color[] colorData;

    /**
     * simple constructor that initializes sliderData and ColorData
     */
    public FractalGenerator() {
        colorData = new Color[2];
        sliderData = new int[6];
    }

    /**
     * Notifies all registered observers of changes to the fractal data
     */
    @Override
    public void notifyObservers() {
        for (FractalObserver observer : observers) {
            observer.update();
        }
    }

    /** adds/registers an observer to the observer list */
    @Override
    public void registerObserver(FractalObserver obs) {
        observers.add(obs);
    }

    /** removes/unregisters an observer from the observer list */
    @Override
    public void unregisterObserver(FractalObserver obs) {
        observers.remove(obs);
    }

    /**
     * Sets the options for the fractal generation based on input
     *
     * @param sliderData  Array of slider data that controls parameters/behaviour for fractal generation
     * @param colorData   Array of color data used to control fractal color
     */
    @Override
    public void setOptions(int[] sliderData, Color[] colorData) {
        this.sliderData = sliderData;
        this.colorData = colorData;

        fractalElements.clear();
        addBranchAndPrepChildren(500, 800, this.sliderData[0], this.sliderData[4], this.sliderData[5], -90);
        notifyObservers();
    }

    /**
     * Returns the list of fractal elements
     *
     * @return list of fractal elements
     */
    @Override
    public ArrayList<FractalElement> getFractalElements() {
        return fractalElements;
    }

    /**
     * Recursively generates branches of the fractal tree
     *
     * @param x                the x position of the starting point of branch
     * @param y                the y position of the starting point of branch
     * @param recursionDepth   the depth of the recursion
     * @param trunkLength      the length of the trunk of current branch
     * @param trunkWidth       the width of the trunk of current branch
     * @param angle            The angle at which the branch is drawn
     */
    private void addBranchAndPrepChildren(int x, int y, int recursionDepth, int trunkLength, int trunkWidth, double angle) {
        if (recursionDepth == 0) {
            return;
        }
        int x2 = (int) (x + trunkLength * Math.cos(Math.toRadians(angle)));
        int y2 = (int) (y + trunkLength * Math.sin(Math.toRadians(angle)));
        Color newColor = getColor(colorData[0], colorData[1], recursionDepth, sliderData[0]);
        Branch branch = new Branch(x, y, x2, y2, trunkWidth, newColor);
        fractalElements.add(branch);
        addBranchAndPrepChildren(x2, y2, recursionDepth - 1, trunkLength * sliderData[1] / 100,
                trunkWidth * sliderData[1] / 100, angle - sliderData[2]);
        addBranchAndPrepChildren(x2, y2, recursionDepth - 1, trunkLength * sliderData[1] / 100,
                trunkWidth * sliderData[1] / 100, angle + sliderData[3]);
    }

    /**
     * Calculates the color based on the initial and final color
     *
     * @param initialColor  the initial color at depth 0
     * @param finalColor    the final color at max value of depth
     * @param depth         the current depth
     * @param finalDepth    the final/max depth
     * @return              The calculated color
     */
    private Color getColor(Color initialColor, Color finalColor, int depth, int finalDepth) {
        float coefficient = (float) depth/finalDepth;
        int red = (int) (initialColor.getRed() * (1 - coefficient) + finalColor.getRed() * coefficient);
        int green = (int) (initialColor.getGreen() * (1 - coefficient) + finalColor.getGreen() * coefficient);
        int blue = (int) (initialColor.getBlue() * (1 - coefficient) + finalColor.getBlue() * coefficient);
        return new Color(red, green, blue);
    }
}